'use strict';

angular.module('digitalprint.app')
    .controller('printshop.GroupsCtrl', function ($scope, $rootScope, $filter, PsGroupService,
                                                  DpCategoryService, GroupDescriptionsService,
                                                  TaxService, $cacheFactory, $state,
                                                  Notification, $modal, FileUploader, $config, ThumbsWidgetService,
                                                  ApiCollection, $timeout, AuthDataService  ) {

        var relType = 1;
        $scope.uploader = [];
        $scope.selectedFiles = [];
        $scope.searchForm = {};

        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        function init() {

            $scope.groups = [];
            $scope.categoriesContains = {};
            $scope.categories = [];
            $scope.groupDescriptions = [];

            $scope.rangeTypes = [
                {
                    name: $filter('translate')('no_rounding'),
                    code: 0
                },
                {
                    name: $filter('translate')('net_prices'),
                    code: 1
                },
                {
                    name: $filter('translate')('gross_prices'),                    code: 2
                }
            ];

            PsGroupService.getAll().then(function (data) {
                $scope.groups = data;
                getCategories();
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        }

        init();


                            $scope.uploadIcon = function (group) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new FileUploader({
                                    'url': PsGroupService.getUploadUrl(),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter',
                                    fn: function (item, options) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop();
                                        var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg','webp'];

                                        if (possibleExtensions.indexOf(lastItem) > -1) {
                                            return true;
                                        }
                                        Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                                        return false;
                                    }
                                });

                                $scope.ok = function () {

                                    var file = uploader.queue[0];
                                    $scope.file = file;

                                    var formData = [];

                                    formData.push({'groupID': group.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response == true) {
                                            group.icon = response.icon;

                                            $scope.form.icon = response.icon;
                                            $scope.form.iconID = response.icon.ID;
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.success($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                                    } else {
                                        $modalInstance.close();
                                    }
                                }
                            }
                        });
                    };

                    $scope.deleteIcon = function (group) {

                        PsGroupService.deleteIcon(group.ID).then(function (data) {
                            if (data.response) {
                                group.icon = null;

                                $scope.form.icon = null;
                                Notification.success($filter('translate')('deleted_successful'));
                            }
                        });

                    };


        $scope.typesLimit = 10;

        var typesConfig = {
            params: {
                limit: $scope.typesLimit
            },
            onSuccess: function (data) {
                $scope.typesCollection.items = data;
            }
        };

        $scope.typeaheadObject ={
            query : '',
            lang: $rootScope.currentLang.code
        };

        $scope.typesCollection = new ApiCollection('ps_types/searchAll', typesConfig);

        var updateTableTimeout;

        $scope.findType = function (val, type) {
            $scope.typesCollection.params.search = val;
            $scope.typesCollection.params.type = type;
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                return $scope.typesCollection.clearCache().then(function (data) {
                    $scope.typesCollection.items = data;
                    return data;
                });
            }, 300);
            return updateTableTimeout;
        };

        $scope.goToType = function() {
            $state.go('printshop-formats', {groupID: $scope.searchForm.type.groupID, typeID: $scope.searchForm.type.ID});
        };

        function categoriesContains() {
            DpCategoryService.categoryContains(relType).then(function (data) {
                $scope.categoriesContains = data;
                _.each($scope.groups, function (group, gIndex) {
                    var obj = _.where($scope.categoriesContains, {itemID: group.ID});
                    if (obj.length > 0) {

                        if (!angular.isDefined($scope.groups[gIndex].categories)) {
                            $scope.groups[gIndex].categories = [];
                        }
                        $scope.groups[gIndex].categories = _.pluck(obj, 'langs');

                    }
                });
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        function getCategories() {
            DpCategoryService.getAll().then(function (data) {
                $scope.categories = data;
                categoriesContains();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        $scope.refreshGroups = function () {
            PsGroupService.getAll();
        };

        $scope.addGroup = function () {

            PsGroupService.add($scope.form).then(function (data) {
                console.log(data);
                if( data.response ) {
                    $scope.groups.push(data.item);
                    $scope.form = {};
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        var categories;

        $scope.setProductCategory = function (group) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/product-group-category.html',
                scope: $scope,
                resolve: {
                    categories: function () {
                        return DpCategoryService.forView().then(function (data) {
                            //console.log('resolve', data)
                            return data;
                        });
                    },
                    selected: function () {
                        return DpCategoryService.getSelectedToGroup(group.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, categories, selected) {

                    $scope.oryg = group;
                    $scope.form = {};

                    $scope.categories = _.clone(categories, true);

                    _.each($scope.categories, function (cat, index) {

                        if (_.indexOf(selected, cat.ID) >= 0) {
                            $scope.categories[index].selected = 1;
                        } else {
                            $scope.categories[index].selected = 0;
                        }

                        if (angular.isDefined(cat.childs)) {
                            _.each(cat.childs, function (val, chIdx) {
                                if (_.indexOf(selected, val.ID) >= 0) {
                                    $scope.categories[index].childs[chIdx].selected = 1;
                                } else {
                                    $scope.categories[index].childs[chIdx].selected = 0;
                                }
                            });
                        }
                    });

                    $scope.cancel = function () {
                        $modalInstance.dismiss('cancel');
                    };

                    $scope.save = function () {

                        $scope.form.categories = [];

                        _.each($scope.categories, function (cat) {

                            if (cat.selected == 1) {
                                $scope.form.categories.push(cat.ID);
                            }

                            if (angular.isDefined(cat.childs)) {

                                _.each(cat.childs, function (item, chIdx) {
                                    if (item.selected == 1) {
                                        $scope.form.categories.push(item.ID);
                                    }
                                });
                            }
                        });

                        DpCategoryService.setSelectedToGroup(group.ID, $scope.form.categories).then(function (data) {
                            var result = [];

                            var gIndex = _.findIndex($scope.groups, {'ID': group.ID});

                            if (gIndex > -1) {
                                _.each(data, function (catID) {

                                    var cIndex = _.findIndex($scope.categories, {'ID': catID});
                                    if (cIndex > -1) {
                                        result.push($scope.categories[cIndex]);
                                    } else {
                                        _.each($scope.categories, function (cat, cIndex) {
                                            var chCat = _.findWhere(cat.childs, {'ID': catID});

                                            if (angular.isDefined(chCat)) {
                                                result.push(chCat);
                                            }
                                        });
                                    }

                                });

                                if (!angular.isDefined($scope.groups[gIndex].categories)) {
                                    $scope.groups[gIndex].categories = [];
                                }
                                $scope.groups[gIndex].categories = _.pluck(result, 'langs');
                            }

                            $modalInstance.dismiss('cancel');
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                }
            });
        };

        $scope.editStart = function (elem) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-group.html',
                scope: $scope,
                resolve: {
                    taxes: function () {
                        return TaxService.getBy(elem.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, taxes) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);
                    $scope.form.taxes = taxes;
                    $scope.save = function () {
                        PsGroupService.edit($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.groups, {ID: $scope.form.ID});
                            if (idx > -1 && data.response) {
                                $scope.groups[idx] = data.item;
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.uploadIcon = function (group) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new FileUploader({
                                    'url': PsGroupService.getUploadUrl(),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter',
                                    fn: function (item, options) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop();
                                        var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg','webp'];

                                        if (possibleExtensions.indexOf(lastItem) > -1) {
                                            return true;
                                        }
                                        Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                                        return false;
                                    }
                                });

                                $scope.ok = function () {

                                    var file = uploader.queue[0];
                                    $scope.file = file;

                                    var formData = [];

                                    formData.push({'groupID': group.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response == true) {
                                            group.icon = response.icon;

                                            var groupIdx = _.findIndex($scope.groups, {ID: group.ID});
                                            if (groupIdx > -1) {
                                                $scope.groups[groupIdx].icon = response.icon;
                                            }
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.success($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                                    } else {
                                        $modalInstance.close();
                                    }
                                }
                            }
                        });
                    };

                    $scope.deleteIcon = function (group) {

                        PsGroupService.deleteIcon(group.ID).then(function (data) {
                            if (data.response) {
                                group.icon = null;
                                var groupIdx = _.findIndex($scope.groups, {ID: group.ID});
                                if (groupIdx > -1) {
                                    $scope.groups[groupIdx].icon = null;
                                    Notification.success($filter('translate')('deleted_successful'));
                                }
                            }
                        });

                    };

                }
            })
        };

        $scope.editCardGuide = function (elem) {

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-group-card-guide.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);
                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.save = function () {


                        PsGroupService.editCardGuide($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.cardGuide, {ID: $scope.form.ID});
                            if (idx > -1) {
                                $scope.groups[idx] = angular.copy($scope.form);
                            }
                            elem.cardGuide = $scope.form.cardGuide;
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                        $modalInstance.close();
                    }

                }

            });
        };

        $scope.removeGroup = function (elem) {

            PsGroupService.remove(elem).then(function (data) {
                var idx = _.findIndex($scope.groups, {ID: elem.ID});
                if (idx > -1) {
                    $scope.groups.splice(idx, 1);
                }
                Notification.success($filter('translate')('removed') + " " + elem.name);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.editDescriptions = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-group-descriptions.html',
                scope: $scope,

                resolve: {
                    allDescriptions: function () {

                        return GroupDescriptionsService.getAll(elem.ID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }

                },
                controller: function ($scope, $modalInstance, allDescriptions) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);
                    $scope.sortChange = false;
                    $scope.descriptionSortableOptions = {
                        opacity: 0.7,
                        axis: 'y',
                        placeholder: 'success',
                        stop: function (e, ui) {

                            var idx = _.findIndex($scope.groupDescriptions, {
                                ID: $scope.groupDescriptions.ID
                            });
                            if (idx > -1) {
                                _.each($scope.groupDescriptions, function (item, index) {
                                    item.order = index;
                                });
                            }

                            $scope.sortChange = true;
                        },
                        handle: 'button.button-sort',
                        cancel: ''
                    };

                    if (allDescriptions.descriptions == null) {
                        $scope.groupDescriptions = [];
                    } else {
                        $scope.groupDescriptions = allDescriptions.descriptions;
                    }
                    $scope.groupDescriptionsTypes = allDescriptions.descTypes;
                    _.each($scope.groupDescriptions, function (item) {
                        //console.log($scope.groupDescriptionsTypes);
                        var idx = _.findIndex($scope.groupDescriptionsTypes, {
                            ID: item.descType
                        });
                        if (idx > -1) {
                            item.descTypeName = $scope.groupDescriptionsTypes[idx].name;
                        }

                    });

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.sortGroupDescSave = function () {

                        var result = [];
                        _.each($scope.groupDescriptions, function (item) {
                            result.push(item.descID);
                        });
                        GroupDescriptionsService.sort(result).then(function (data) {
                            $scope.sortChange = false;
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            $scope.sortGroupDescCancel();
                        });
                    };
                    $scope.sortGroupDescCancel = function () {
                        $scope.sortChange = false;
                    };
                    $scope.save = function () {
                        GroupDescriptionsService.create($scope.form, $scope.showLang).then(function (data) {
                            data.groupID = elem.ID;
                            _.each(allDescriptions.descTypes, function (item) {
                                var idx = _.findIndex(allDescriptions.descTypes, {
                                    ID: data.descType
                                });
                                data.descTypeName = allDescriptions.descTypes[idx].name;
                            });
                            $scope.groupDescriptions.push(data);
                            $scope.form.groupDescriptions.langs = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.delete = function (elem) {
                        GroupDescriptionsService.removeDescription(elem.descID).then(function (data) {
                            var idx = _.findIndex($scope.groupDescriptions, {
                                ID: elem.ID
                            });
                            $scope.groupDescriptions.splice(idx, 1);
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));

                        });
                    }


                }

            });
        };

        $scope.thumbs = function (elem) {
            ThumbsWidgetService.getThumbsModal($scope, elem, GroupDescriptionsService);
        };


        $scope.checkDescriptionType = function (elem) {
            if (elem.descType === 1) {
                $scope.editDescription(elem);
            } else {
                $scope.thumbs(elem);
            }
        };

        $scope.editDescription = function (elem) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-type-description.html',
                scope: $scope,
                resolve: {
                    allDescriptions: function () {

                        return GroupDescriptionsService.getAll(elem.groupID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, allDescriptions) {
                    if (allDescriptions.descriptions == null) {
                        $scope.groupDescriptions = [];
                    } else {
                        $scope.groupDescriptions = allDescriptions.descriptions;
                    }
                    var idx = _.findIndex($scope.groupDescriptions, {
                        ID: elem.ID
                    });
                    $scope.form = $scope.groupDescriptions[idx];
                    $scope.save = function () {

                        GroupDescriptionsService.editDescription($scope.form).then(function (data) {
                            if (idx > -1) {
                                $scope.groupDescriptions[idx] = $scope.form;
                                elem = $scope.form;
                            }
                            Notification.success($filter('translate')('success'));
                        });
                    };
                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }

            });

        }
    });