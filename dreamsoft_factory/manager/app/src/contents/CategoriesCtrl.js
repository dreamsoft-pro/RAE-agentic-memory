angular.module('digitalprint.app')
    .controller('contents.CategoriesCtrl', function ($scope, $filter, $modal, DpCategoryService,
                                                     CategoryDescriptionsService, SubcategoryDescriptionsService,
                                                     Notification, FileUploader, ThumbsWidgetService,
                                                     DiscountService, $q, $config, AuthDataService,MetaTagService) {

        $scope.categoryForm = {};
        $scope.uploader = [];
        $scope.selectedFiles = [];
        $scope.discountGroups = [];
        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        function getCategories() {
            DpCategoryService.getAll().then(function (data) {
                $scope.categories = data;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        function init() {

            $scope.sortChange = false;
            $scope.card_opt = [{
                name: $filter('translate')('twitter_summary'), code: 'twitter_summary'
            }, {
                name: $filter('translate')('twitter_summary_large_image'), code: 'twitter_summary_large_image'
            }, {
                name: $filter('translate')('empty'), code: ''
            }];
            $scope.sortableOptions = {
                opacity: 0.7,
                axis: 'y',
                placeholder: 'success',
                stop: function (e, ui) {
                    _.each($scope.categories, function (item, index) {
                        item.sort = index;
                    });
                    $scope.sortChange = true;
                },
                handle: 'button.button-sort',
                cancel: ''
            };

            getCategories();

            getDiscountGroups().then( function(discountGroups) {
                $scope.discountGroups = discountGroups;
            });
        }

        function getDiscountGroups()
        {
            var def = $q.defer();

            DiscountService.getGroups().then(function (data) {
                def.resolve(data);
            });

            return def.promise;
        }

        init();

        $scope.save = function () {

            DpCategoryService.create($scope.categoryForm).then(function (data) {
                if (data.response == true) {
                    if (data.item.parentID > 0) {
                        var idx = _.findIndex($scope.categories, {ID: data.item.parentID});
                        if (idx > -1) {
                            $scope.categories[idx].childs.push(data.item);
                        }
                    } else {
                        $scope.categories.push(data.item);
                    }

                    $scope.categoryForm = {};

                    Notification.success($filter('translate')('success'));
                } else {

                    if (data.invalidSlugs && data.invalidSlugs.length > 0) {
                        Notification.warning($filter('translate')('repeated_name_of_url') + ' - ' + data.invalidSlugs.join(', '));
                    } else {
                        Notification.error($filter('translate')('error'));
                    }


                }


            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.refresh = function (fromCache) {

        };

        $scope.editStart = function (category) {

            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-category.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.form = _.clone(category, true);

                    if (  category.images === undefined || category.images === []){
                        $scope.images = {};
                    }
                    else {
                        $scope.images = category.images;
                    }

                    $scope.save = function () {
                        DpCategoryService.edit($scope.form).then(function (data) {
                            if (data.item) {
                                if (data.item.parentID > 0) {
                                    var idx = _.findIndex($scope.categories, {ID: data.item.parentID});
                                    if (idx > -1) {
                                        var idxCh = _.findIndex($scope.categories[idx].childs, {ID: data.item.ID});
                                        if (idxCh > -1) {
                                            $scope.categories[idx].childs[idxCh].langs = data.item.langs;
                                            $scope.categories[idx].childs[idxCh].active = data.item.active;
                                            $scope.categories[idx].childs[idxCh].metatags = data.item.metatags;
                                            $scope.categories[idx].childs[idxCh].icons = data.item.icons;
                                            $scope.categories[idx].childs[idxCh].discountGroupNames = data.item.discountGroupNames;
                                            $scope.categories[idx].childs[idxCh].onMainPage = data.item.onMainPage;
                                            $scope.categories[idx].childs[idxCh].discountGroupID = data.item.discountGroupID;
                                        }
                                    }
                                } else {
                                    var idx = _.findIndex($scope.categories, {ID: data.item.ID});
                                    if (idx > -1) {
                                        $scope.categories[idx].langs = data.item.langs;
                                        $scope.categories[idx].active = data.item.active;
                                        $scope.categories[idx].metatags = data.item.metatags;
                                        $scope.categories[idx].icons = data.item.icons;
                                        $scope.categories[idx].discountGroupNames = data.item.discountGroupNames;
                                        $scope.categories[idx].onMainPage = data.item.onMainPage;
                                        $scope.categories[idx].discountGroupID = data.item.discountGroupID;
                                    }
                                }
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            }

                        }, function (data) {
                            if (data.invalidSlugs && data.invalidSlugs.length > 0) {
                                Notification.warning($filter('translate')('repeated_name_of_url') + ' - ' + data.invalidSlugs.join(', '));
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };


                    $scope.uploadImage = function ( images, lang, form) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/image-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            resolve: {
                                images: function () {
                                    return images;
                                },
                                   lang: function () {
                                    return lang;
                                }, form: function () {
                                    return form;
                                },
                            },
                            controller: function ($scope, $modalInstance, lang, form) {
                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();
                                var uploader = $scope.uploader = new FileUploader({
                                    'url': MetaTagService.getUploadUrl('dp_metaTags'),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter', fn: function (item) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop().toLowerCase();
                                        var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg', 'webp'];

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
                                    // ensure that lang entry exist

                                    if (form.metatags[lang]===undefined){
                                        form.metatags[lang] = {};
                                    }
                                    formData.push({'metatagID': form.metatags[lang].ID});
                                    formData.push({'language': lang});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response) {
                                        if (response.response === true) {

                                            form.metatags[response.lang].imageID = response.image.ID;
                                            images[response.image.ID] = response.image;
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.error($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        Notification.warning($filter('translate')('uploading_in_progress'));
                                    } else {
                                        $modalInstance.close();
                                    }
                                };
                            }
                        });
                    };
                    $scope.deleteImage = function ( images, lang, form) {
                        MetaTagService.deleteImage(lang, form.metatags[lang].imageID,'dp_metaTags').then(function (data) {

                            if (data.response) {
                                form.metatags[lang].imageID = null;
                                delete images[form.metatags[lang].imageID] ;
                                Notification.success($filter('translate')('deleted_successful'));

                            }
                        });

                    };



                }

            });
        };

        $scope.editChilds = function (category) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/list-subcategories.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.category = category;
                    $scope.childs = category.childs;

                    $scope.form = {};
                    $scope.form.parentID = category.ID;

                    $scope.sortChange = false;

                    $scope.sortableOptions = {
                        opacity: 0.7,
                        axis: 'y',
                        placeholder: 'success',
                        stop: function (e, ui) {
                            var idx = _.findIndex($scope.categories, {ID: category.ID});
                            if (idx > -1) {

                                _.each($scope.categories[idx].childs, function (item, index) {
                                    item.sort = index;
                                });
                            }

                            $scope.sortChange = true;
                        },
                        handle: 'button.button-sort',
                        cancel: ''
                    };

                    $scope.save = function () {
                        DpCategoryService.create($scope.form).then(function (data) {
                            if (data.item) {
                                $scope.category.childs.push(data.item);
                                Notification.success($filter('translate')('success'));
                            } else {

                                if (data.invalidSlugs && data.invalidSlugs.length > 0) {
                                    Notification.warning($filter('translate')('repeated_name_of_url') + ' - ' + data.invalidSlugs.join(', '));
                                } else {
                                    Notification.error($filter('translate')('error'));
                                }

                            }

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.delete = function (category) {
                        DpCategoryService.delete(category).then(function (data) {

                            Notification.success($filter('translate')('removed') + " " + data.ID);
                            var idx = _.findIndex($scope.childs, {ID: category.ID});
                            if (idx > -1) {
                                $scope.childs.splice(idx, 1);
                            }
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.sortSave = function () {
                        var result = [];
                        var idx = _.findIndex($scope.categories, {ID: category.ID});
                        if (idx > -1) {
                            var cats = _.sortBy($scope.categories[idx].childs, function (p) {
                                return p.sort
                            });
                            _.each(cats, function (item, index) {
                                result.push(item.ID);
                            });

                            DpCategoryService.sort(result).then(function (data) {
                                $scope.sortChange = false;
                                Notification.success($filter('translate')('success'));
                            }, function (data) {
                                Notification.error($filter('translate')('error'));
                                $scope.sortCancel();
                            });
                        }


                    };

                    $scope.sortCancel = function () {
                        $scope.sortChange = false;
                    }

                }

            })
        };

        $scope.delete = function (category) {

            DpCategoryService.delete(category).then(function (data) {

                Notification.success($filter('translate')('removed') + " " + data.ID);
                var idx = _.findIndex($scope.categories, {ID: category.ID});
                if (idx > -1) {
                    $scope.categories.splice(idx, 1);
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.sortSave = function () {
            var result = [];
            var cats = _.sortBy($scope.categories, function (p) {
                return p.sort
            });
            _.each(cats, function (item, index) {
                result.push(item.ID);
            });

            DpCategoryService.sort(result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.sortCancel = function () {
            $scope.sortChange = false;
        };

        $scope.editDescriptions = function (elem) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-category-descriptions.html',
                scope: $scope,

                resolve: {
                    allDescriptions: function () {
                        return CategoryDescriptionsService.getAll(elem.ID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }

                },
                controller: function ($scope, $modalInstance, allDescriptions) {
                    $scope.currentCat = elem;
                    $scope.form = angular.copy(elem);
                    $scope.images = {};
                    $scope.sortChange = false;
                    $scope.descriptionSortableOptions = {
                        opacity: 0.7,
                        axis: 'y',
                        placeholder: 'success',
                        stop: function (e, ui) {

                            var idx = _.findIndex($scope.categoryDescriptions, {
                                ID: $scope.categoryDescriptions.ID
                            });
                            if (idx > -1) {
                                _.each($scope.categoryDescriptions, function (item, index) {
                                    item.order = index;
                                });
                            }

                            $scope.sortChange = true;
                        },
                        handle: 'button.button-sort',
                        cancel: ''
                    };

                    if (allDescriptions.descriptions == null) {
                        $scope.categoryDescriptions = [];
                    } else {
                        $scope.categoryDescriptions = allDescriptions.descriptions;
                    }
                    $scope.categoryDescriptionsTypes = allDescriptions.descTypes;
                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.sortCategoryDescSave = function () {

                        var result = [];
                        _.each($scope.categoryDescriptions, function (item) {
                            result.push(item.descID);
                        });
                        CategoryDescriptionsService.sort(result).then(function (data) {
                            $scope.sortChange = false;
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            $scope.sortCategoryDescCancel();
                        });
                    };
                    $scope.sortCategoryDescCancel = function () {
                        $scope.sortChange = false;
                    };
                    $scope.save = function () {
                        CategoryDescriptionsService.create($scope.form, $scope.form.showLang).then(function (data) {
                            data.categoryID = elem.ID;
                            $scope.categoryDescriptions.push(data);
                            _.each(allDescriptions.descTypes, function (item) {
                                var idx = _.findIndex(allDescriptions.descTypes, {
                                    ID: data.descType
                                });
                                data.descTypeName = allDescriptions.descTypes[idx].name;
                            });
                            $scope.form.categoryDescriptions.langs = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.delete = function (elem) {
                        CategoryDescriptionsService.removeDescription(elem.descID).then(function (data) {
                            var idx = _.findIndex($scope.categoryDescriptions, {
                                ID: elem.ID
                            });
                            $scope.categoryDescriptions.splice(idx, 1);
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));

                        });
                    }


                }

            });
        };

        $scope.editDescription = function (elem, catID) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-type-description.html',
                scope: $scope,
                resolve: {
                    allDescriptions: function () {

                        return CategoryDescriptionsService.getAll(catID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, allDescriptions) {

                    $scope.categoryDescriptions = allDescriptions.descriptions;
                    var idx = _.findIndex($scope.categoryDescriptions, {
                        ID: elem.ID
                    });
                    $scope.form = $scope.categoryDescriptions[idx];
                    $scope.save = function () {

                        CategoryDescriptionsService.editDescription($scope.form).then(function (data) {
                            if (idx > -1) {
                                $scope.categoryDescriptions[idx] = $scope.form;
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

        };

        $scope.thumbs = function (elem) {
            ThumbsWidgetService.getThumbsModal($scope, elem, CategoryDescriptionsService);
        };

        $scope.checkDescriptionType = function (elem, catID) {
            if (elem.descType === 1) {
                $scope.editDescription(elem, catID);
            } else {
                $scope.thumbs(elem, catID);
            }
        };

        $scope.editChildDescriptions = function (elem) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-subcategory-descriptions.html',
                scope: $scope,
                resolve: {
                    allDescriptions: function () {
                        return SubcategoryDescriptionsService.getAll(elem.ID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }

                },
                controller: function ($scope, $modalInstance, allDescriptions) {
                    $scope.currentSubcat = elem;
                    $scope.form = angular.copy(elem);
                    $scope.sortChange = false;
                    $scope.descriptionSortableOptions = {
                        opacity: 0.7,
                        axis: 'y',
                        placeholder: 'success',
                        stop: function (e, ui) {

                            var idx = _.findIndex($scope.subcategoryDescriptions, {
                                ID: $scope.subcategoryDescriptions.ID
                            });
                            if (idx > -1) {
                                _.each($scope.subcategoryDescriptions, function (item, index) {
                                    item.order = index;
                                });
                            }

                            $scope.sortChange = true;
                        },
                        handle: 'button.button-sort',
                        cancel: ''
                    };

                    if (allDescriptions.descriptions == null) {
                        $scope.subcategoryDescriptions = [];
                    } else {
                        $scope.subcategoryDescriptions = allDescriptions.descriptions;
                    }
                    $scope.subcategoryDescriptionsTypes = allDescriptions.descTypes;
                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.sortSubcategoryDescSave = function () {

                        var result = [];
                        _.each($scope.subcategoryDescriptions, function (item) {
                            result.push(item.descID);
                        });
                        SubcategoryDescriptionsService.sort(result).then(function (data) {
                            $scope.sortChange = false;
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            $scope.sortSubcategoryDescCancel();
                        });
                    };
                    $scope.sortSubcategoryDescCancel = function () {
                        $scope.sortChange = false;
                    };
                    $scope.save = function () {
                        SubcategoryDescriptionsService.create($scope.form, $scope.form.showLang).then(function (data) {
                            data.categoryID = elem.ID;
                            $scope.subcategoryDescriptions.push(data);

                            $scope.form.subcategoryDescriptions.langs = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.delete = function (elem) {
                        SubcategoryDescriptionsService.removeDescription(elem.descID).then(function (data) {
                            var idx = _.findIndex($scope.subcategoryDescriptions, {
                                ID: elem.ID
                            });
                            $scope.subcategoryDescriptions.splice(idx, 1);
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));

                        });
                    }


                }

            });
        };

        $scope.editChildDescription = function (elem, subCatID) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-type-description.html',
                scope: $scope,
                resolve: {
                    allDescriptions: function () {

                        return SubcategoryDescriptionsService.getAll(subCatID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, allDescriptions) {
                    if (allDescriptions.descriptions == null) {
                        $scope.subcategoryDescriptions = {};
                    } else {
                        $scope.subcategoryDescriptions = allDescriptions.descriptions;
                    }
                    var idx = _.findIndex($scope.subcategoryDescriptions, {
                        ID: elem.ID
                    });
                    $scope.form = $scope.subcategoryDescriptions[idx];
                    $scope.save = function () {

                        SubcategoryDescriptionsService.editDescription($scope.form).then(function (data) {
                            if (idx > -1) {
                                $scope.subcategoryDescriptions[idx] = $scope.form;
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

        };
        $scope.childThumbs = function (elem) {
            ThumbsWidgetService.getThumbsModal($scope, elem, SubcategoryDescriptionsService);
        };
        $scope.checkChildDescriptionType = function (elem, subcatID) {
            if (elem.descType === 1) {
                $scope.editChildDescription(elem, subcatID);
            } else {
                $scope.thumbs(elem, subcatID);
            }
        };

        $scope.uploadIcon = function (category) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                scope: $scope,
                backdrop: 'static',
                keyboard: false,
                controller: function ($scope, $modalInstance) {

                    var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

                    var header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();

                    var uploader = $scope.uploader = new FileUploader({
                        'url': DpCategoryService.getUploadUrl(),
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

                        formData.push({'categoryID': category.ID});
                        file.formData = formData;

                        uploader.uploadItem(file);

                        uploader.onSuccessItem = function (fileItem, response, status, headers) {
                            if (response.response === true) {
                                category.icon = response.icon;
                                var catIdx = 0;
                                if (category.parentID > 0) {
                                    catIdx = _.findIndex($scope.categories, {ID: category.parentID});
                                } else {
                                    catIdx = _.findIndex($scope.categories, {ID: category.ID});
                                }

                                if (catIdx > -1) {
                                    if (response.item.parentID > 0) {
                                        var idxCh = _.findIndex($scope.categories[catIdx].childs, {ID: category.ID});
                                        if (idxCh > -1) {
                                            $scope.categories[catIdx].childs[idxCh].icon = response.icon;
                                        }
                                    } else {
                                        $scope.categories[catIdx].icon = response.icon;
                                    }
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

            DpCategoryService.deleteIcon(group.ID).then(function (data) {
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

    });
