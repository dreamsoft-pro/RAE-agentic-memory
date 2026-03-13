angular.module('digitalprint.app')
    .controller('printshop.TypesCtrl', function ($rootScope, $filter, $scope, $stateParams, $modal, $state, $q, Notification,
                                                 PsTypeService, TaxService, PsGroupService, DpCategoryService,
                                                 TypeDescriptionsService, TypeDescriptionsFormatsService,
                                                 PsFormatService, FileUploader, ModelIconsService, TypePatternService,
                                                 LangSettingsService, PsComplexService,
                                                 $config, ThumbsWidgetService, AuthDataService, PsPricelistService,
                                                 PsConfigAttributeNatureService, MarginsService, MetaTagService ) {

        var currentGroupID;
        var relType = 2;
        var FormatService;
        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;
        $scope.formats = [];
        $scope.uploader = [];
        $scope.selectedFiles = [];
        $scope.STATIC_URL = $config.STATIC_URL;
        $scope.marginForm = {};
        $scope.uploadIcon = function (type) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                scope: $scope,
                backdrop: 'static',
                keyboard: false,
                controller: function ($scope, $modalInstance) {

                    var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

                    var header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();

                    var uploader = $scope.uploader = new
                    FileUploader({
                        'url': PsTypeService.getUploadUrl(),
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

                        formData.push({'typeID': type.ID});
                        file.formData = formData;

                        uploader.uploadItem(file);

                        uploader.onSuccessItem = function (fileItem, response, status, headers) {
                            if (response.response == true) {
                                type.icon = response.icon;
                                $scope.form.icon = response.icon;
                                $scope.form.iconID = response.icon.ID
                                console.log($scope.form.iconID);
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
        $scope.deleteIcon = function (type) {

            PsTypeService.deleteIcon(type.ID).then(function (data) {
                if (data.response) {
                    type.icon = null;
                    var typeIdx = _.findIndex($scope.types, {ID: type.ID});
                    if (typeIdx > -1) {
                        $scope.types[typeIdx].icon = null;
                        Notification.success($filter('translate')('deleted_successful'));
                    }
                }
            });

        };
        function init() {
            $scope.showAllTypes = $state.current.name == 'printshop-group-types';
            $scope.form = {};
            $scope.types = [];
            $scope.categoriesContains = {};
            $scope.categories = [];
            $scope.typeDescriptions = [];

            currentGroupID = $scope.currentGroupID = $stateParams.groupID ? parseInt($stateParams.groupID): '';

            $scope.sortChange = false;

            PsPricelistService.getAll().then(function (data) {
                $scope.priceList = data;
            }, function (error) {
                console.error(error)
            });

            PsConfigAttributeNatureService.getAll().then(function (data) {
                $scope.natures = data;
            });

            $q.all([PsGroupService.getAll(), PsTypeService.getAll(currentGroupID)]).then(function (data) {
                $scope.groups = data[0];
                if (!$scope.showAllTypes) {
                    $scope.group = _.findWhere($scope.groups, {
                        ID: currentGroupID
                    });
                    $rootScope.currentGroupName = $scope.group.name;
                }
                $scope.types = data[1];
                DpCategoryService.getAll().then(function (data) {
                    $scope.categories = data;
                    categoriesContains();
                });
                _.each($scope.types, function (type) {
                    var group = _.find($scope.groups, function (group) {
                        return group.ID == type.groupID;
                    });
                    if (group) {
                        type.groupName = group.name;
                        type.sortGroup = _.findIndex($scope.groups, group);
                    }
                });
                $scope.types = _.sortBy($scope.types,'sortGroup');
            });

            TaxService.getAll().then(function (data) {

                $scope.taxes = data;

                var defTax = _.findWhere($scope.taxes, {
                    default: 1
                });

                if (defTax != undefined) {

                    $scope.defaultTax = _.findWhere($scope.taxes, {
                        default: 1
                    });

                }

            });

            $scope.sortableOptions = {
                stop: function (e, ui) {
                    $scope.sortChange = true;
                },
                axis: 'y',
                placeholder: 'success',
                handle: 'button.button-sort',
                cancel: ''
            };

        }

        init();

        function categoriesContains() {
            DpCategoryService.categoryContains(relType).then(function (data) {
                $scope.categoriesContains = data;
                _.each($scope.types, function (type, gIndex) {
                    var obj = _.where($scope.categoriesContains, {
                        itemID: type.ID
                    });
                    if (obj.length > 0) {

                        if (!angular.isDefined($scope.types[gIndex].categories)) {
                            $scope.types[gIndex].categories = [];
                        }
                        $scope.types[gIndex].categories = _.pluck(obj, 'langs');

                    }
                });
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        $scope.refreshTypes = function () {
            PsTypeService.getAll(currentGroupID, true).then(function (data) {
                $scope.types = data;
            });
        };

        $scope.addType = function () {

            PsTypeService.add(currentGroupID, $scope.form).then(function (data) {
                if( data.response ) {
                    $scope.form = {};
                    Notification.success($filter('translate')('success'));
                    $scope.refreshTypes();
                } else {
                    Notification.error($filter('translate')('error'));
                }

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.editStart = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-type.html',
                scope: $scope,
                resolve: {
                    taxes: function () {
                        return TaxService.getBy(currentGroupID, elem.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, taxes) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);
                    console.log($scope.form);
                    $scope.form.taxes = taxes;

                    if (  elem.images === undefined || elem.images === []){
                        $scope.images = {};
                    }
                    else {
                        $scope.images = elem.images;
                    }

                    $scope.save = function () {

                        PsTypeService.edit(currentGroupID, $scope.form).then(function (data) {

                            var idx = _.findIndex($scope.types, {
                                ID: $scope.form.ID
                            });

                            if (idx > -1 && data.response) {
                                $scope.types[idx] = data.item;
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

                    $scope.uploadIcon = function (type) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new
                                FileUploader({
                                    'url': PsTypeService.getUploadUrl(),
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

                                    formData.push({'typeID': type.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response == true) {
                                            type.icon = response.icon;

                                            var typeIdx = _.findIndex($scope.types, {ID: type.ID});
                                            if (typeIdx > -1) {
                                                $scope.types[typeIdx].icon = response.icon;
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

                    $scope.deleteIcon = function (type) {

                        PsTypeService.deleteIcon(type.ID).then(function (data) {
                            if (data.response) {
                                type.icon = null;
                                var typeIdx = _.findIndex($scope.types, {ID: type.ID});
                                if (typeIdx > -1) {
                                    $scope.types[typeIdx].icon = null;
                                    Notification.success($filter('translate')('deleted_successful'));
                                }
                            }
                        });

                    };

                }
            });


            $scope.uploadImage = function ( images, form, lang) {
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
                    controller: function ($scope, $modalInstance, images, form, lang) {
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
                            if (form.metaTags[lang]===undefined){
                                form.metaTags[lang]= {};
                            }
                            var formData = [];
                            formData.push({'metatagID': form.metaTags[lang].ID});
                            formData.push({'language': lang});

                            file.formData = formData;

                            uploader.uploadItem(file);

                            uploader.onSuccessItem = function (fileItem, response) {
                                console.log(form.metaTags,images);

                                if (response.response === true) {
                                    if (form.metaTags[lang]===undefined){
                                        form.metaTags[lang]= {};
                                    }
                                    form.metaTags[lang].imageID = response.image.ID;
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
            $scope.deleteImage = function ( images, form, lang, imageID) {
                MetaTagService.deleteImage(lang, imageID ,'dp_metaTags').then(function (data) {
                    if (data.response) {
                        form.metaTags[lang].imageID = null;
                        delete images[form.metaTags[lang].imageID] ;
                        Notification.success($filter('translate')('deleted_successful'));

                    }
                });
            };

        };


        $scope.editCardGuide = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-type-card-guide.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = angular.copy(elem);
                    $scope.cancel = function () {
                        $modalInstance.close();
                    };
                    $scope.save = function () {


                        PsTypeService.editCardGuide(currentGroupID, $scope.form).then(function (data) {
                            var idx = _.findIndex($scope.cardGuide, {
                                ID: $scope.form.ID
                            });
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

        $scope.editDescriptions = function (elem) {

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-type-descriptions.html',
                scope: $scope,

                resolve: {
                    allDescriptions: function () {
                        return TypeDescriptionsService.getAll(elem.groupID, elem.ID, $scope.currentLang.code).then(function (data) {
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

                            idx = _.findIndex($scope.typeDescriptions, {
                                ID: $scope.typeDescriptions.ID
                            });

                            if (idx > -1) {
                                _.each($scope.typeDescriptions, function (item, index) {
                                    item.order = index;
                                });
                            }

                            $scope.sortChange = true;
                        },
                        handle: 'button.button-sort',
                        cancel: ''
                    };

                    if (allDescriptions.descriptions == null) {
                        $scope.typeDescriptions = [];
                    } else {
                        $scope.typeDescriptions = allDescriptions.descriptions;
                    }
                    $scope.typeDescriptionsTypes = allDescriptions.descTypes;

                    _.each($scope.typeDescriptions, function (item) {
                        var idx = _.findIndex($scope.typeDescriptionsTypes, {
                            ID: item.descType
                        });
                        if (idx > -1) {
                            item.descTypeName = $scope.typeDescriptionsTypes[idx].name;
                        }

                    });

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };

                    $scope.sortTypeDescSave = function () {

                        var result = [];
                        _.each($scope.typeDescriptions, function (item) {
                            result.push(item.descID);
                        });

                        TypeDescriptionsService.sort(result).then(function (data) {
                            $scope.sortChange = false;
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            $scope.sortTypeDescCancel();
                        });
                    };
                    $scope.sortTypeDescCancel = function () {
                        $scope.sortChange = false;
                    };
                    $scope.save = function () {

                        TypeDescriptionsService.create($scope.form, $scope.showLang).then(function (data) {
                            data.typeID = elem.ID;
                            _.each(allDescriptions.descTypes, function (item) {
                                var idx = _.findIndex(allDescriptions.descTypes, {
                                    ID: data.descType
                                });
                                data.descTypeName = allDescriptions.descTypes[idx].name;
                            });
                            $scope.typeDescriptions.push(data);

                            $scope.form.typeDescriptions.langs = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.delete = function (elem) {
                        TypeDescriptionsService.removeDescription(elem.descID).then(function (data) {
                            var idx = _.findIndex($scope.typeDescriptions, {
                                ID: elem.ID
                            });
                            $scope.typeDescriptions.splice(idx, 1);
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));

                        });
                    }


                }

            });
        };

        $scope.thumbs = function (elem) {
            ThumbsWidgetService.getThumbsModal($scope, elem, TypeDescriptionsService);
        };


        $scope.checkDescriptionType = function (elem) {

            if ([1,8].includes(elem.descType)) {
                $scope.editDescription(elem);
            } else if (elem.descType == 7) {
                $scope.editPatterns(elem)
            } else {
                $scope.thumbs(elem);
            }
        };

        $scope.editPatterns = function (elem) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-patterns.html',
                scope: $scope,
                resolve: {
                    typeFormats: function () {

                        FormatService = new PsFormatService($scope.currentGroupID, elem.typeID);
                        return FormatService.getAll().then(function (data) {
                            return data;
                        });

                    },
                    subProducts: function () {

                        var ComplexService = new PsComplexService($scope.currentGroupID, elem.typeID);
                        return ComplexService.getByBaseID(elem.typeID).then(function (data) {
                            return data;
                        }, function (errorData) {
                            return [];
                        });

                    },
                    patternExtensions: function () {
                        return ModelIconsService.getAll().then(function (data) {
                            return data;
                        });
                    },
                    patterns: function () {
                        return TypePatternService.getList(elem.typeID, elem.descID).then(function (data) {
                            return data;
                        });
                    },
                    langList: function () {
                        return LangSettingsService.getAll().then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, typeFormats, subProducts, patternExtensions,
                                      AuthDataService, patterns, langList) {

                    $scope.langList = langList;
                    $scope.patterns = patterns;

                    var strFileTypes = 'pdf|illustrator|postscript|eps|jpeg|webp|jpg|tif|tiff|wmf|vnd.adobe.photoshop|msword|zip|cdr|jpeg|tiff';
                    var strExtensions = 'pdf|ai|indd|eps|jpg|tif|wmf|psd|doc|zip|cdr|jpeg|webp|tiff';
                    if (patternExtensions.length > 0) {
                        var arrExtensions = [];
                        _.each(patternExtensions, function (ext) {
                            arrExtensions.push(ext.extension)
                        });
                        strExtensions = arrExtensions.join('|');
                    }
                    strFileTypes = '|' + strFileTypes + '|';
                    strExtensions = '|' + strExtensions + '|';

                    if (typeFormats.length > 0) {
                        $scope.typeFormats = typeFormats;
                    } else {
                        $scope.typeFormats = subProducts[0].relatedFormats;
                    }

                    var uploader = $scope.uploader = new FileUploader({
                        'url': TypePatternService.getUploadUrl(),
                        'queueLimit': 1,
                        'autoUpload': false
                    });

                    uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item, options) {
                            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                            var checkType = strFileTypes.indexOf(type) !== -1;
                            var checkExt = false
                            if (!checkType) {
                                Notification.warning($filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, ''));
                            }else{
                                var ext = '|' + item.name.slice(item.name.lastIndexOf('.') + 1)+'|' ;
                                checkExt = strExtensions.indexOf(ext) !== -1;
                                if (!checkExt) {
                                    Notification.warning($filter('translate')('not_supported_ext_of_file') + ' - ' + ext.replace(/\|/g, ''));
                                }
                            }

                            return checkType && checkExt;
                        }
                    });

                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                        $scope.patterns.push(response.pattern);
                        uploader.clearQueue();
                    };

                    uploader.onBeforeUploadItem = function (item) {
                        if (uploader.queue > 0) {
                            Notification.warning('Only one file for pattern!');
                        }
                    };

                    $scope.cancel = function () {
                        if (uploader.isUploading) {
                            alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                        } else {
                            $modalInstance.close();
                        }
                    };

                    var formData;

                    $scope.save = function () {

                        var file = uploader.queue[0];

                        formData = [{
                            'lang': $scope.form.lang,
                            'formatID': $scope.form.formatID,
                            'descID': elem.descID,
                            'typeID': elem.typeID
                        }];

                        file.formData = formData;
                        // TODO co to jest?
                        // file.upload(function (upData) {
                        //     console.log(upData);
                        // });
                    };

                    $scope.delete = function (elem) {
                        TypePatternService.delete(elem.ID).then(function (data) {
                            var idx = _.findIndex($scope.patterns, {
                                ID: elem.ID
                            });
                            $scope.patterns.splice(idx, 1);
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));

                        });
                    };

                    $scope.urlLoad = function (elem) {
                        window.open(elem.patternFile, '_blank');
                    };

                    $scope.clearQueue = function () {
                        uploader.clearQueue();
                    };
                }

            });
        };

        $scope.editDescription = function (elem) {
            $modal.open({

                templateUrl: 'src/printshop/templates/modalboxes/edit-type-description.html',
                scope: $scope,
                resolve: {
                    allDescriptions: function () {

                        return TypeDescriptionsService.getAll($scope.currentGroupID, elem.typeID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, allDescriptions) {

                    $scope.typeDescriptions = allDescriptions.descriptions;

                    var idx = _.findIndex($scope.typeDescriptions, {
                        ID: elem.ID
                    });
                    $scope.form = $scope.typeDescriptions[idx];
                    $scope.save = function () {

                        TypeDescriptionsService.editDescription($scope.form).then(function (data) {
                            if (idx > -1) {
                                $scope.typeDescriptions[idx] = $scope.form;
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

        $scope.typeDescriptionFormats = function (elem) {
            $scope.currentDescID = elem.ID;

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-typedescription-formats.html',
                scope: $scope,
                resolve: {
                    typeFormats: function () {
                        FormatService = new PsFormatService($scope.currentGroupID, elem.typeID);
                        return FormatService.getAll().then(function (data) {
                            return data;
                        });
                    },
                    subProducts: function () {

                        var ComplexService = new PsComplexService($scope.currentGroupID, elem.typeID);
                        return ComplexService.getByBaseID(elem.typeID).then(function (data) {
                            return data;
                        }, function (errorData) {
                            return [];
                        });

                    },
                    descFormats: function () {
                        return TypeDescriptionsFormatsService.getAll(elem.descID).then(function (data) {
                            return data;
                        });
                    },
                    allDescriptions: function () {
                        return TypeDescriptionsService.getAll(elem.groupID, elem.typeID, $scope.currentLang.code).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, typeFormats, allDescriptions, descFormats, subProducts) {
                    var description = descFormats;

                    if (typeFormats.length > 0) {
                        $scope.formats = typeFormats;
                    } else {
                        $scope.formats = subProducts[0].relatedFormats;
                    }

                    $scope.typeDescriptions = allDescriptions.descriptions;
                    $scope.typeDescriptionsFormats = angular.copy($scope.formats);

                    _.each(description, function (item) {
                        _.each($scope.typeDescriptionsFormats, function (descItem) {
                            if (item.formatID == descItem.ID) {
                                descItem.selected = 1;
                            } else {

                            }
                        });
                    });
                    $scope.save = function () {
                        elem.countFormats = 0;
                        _.each($scope.typeDescriptionsFormats, function (item) {
                            if (item.selected == 1) {
                                elem.countFormats++;
                            }
                        });

                        TypeDescriptionsFormatsService.setFormats(elem.descID, $scope.typeDescriptionsFormats).then(function (data) {
                            Notification.success($filter('translate')('success'));

                            $modalInstance.close();
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            });
        };

        $scope.removeType = function (elem) {

            PsTypeService.remove(currentGroupID, elem).then(function (data) {
                var idx = _.findIndex($scope.types, {
                    ID: elem.ID
                });
                if (idx > -1) {
                    $scope.types.splice(idx, 1);
                }
                Notification.success($filter('translate')('removed') + " " + elem.name);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.sortCancel = function () {
            $scope.refreshTypes();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.types, function (item) {
                result.push(item.ID);
            });

            PsTypeService.sort(currentGroupID, result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.setProductCategory = function (type) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/product-group-category.html',
                scope: $scope,
                resolve: {
                    categories: function () {
                        return DpCategoryService.forView().then(function (data) {
                            return data;
                        });
                    },
                    selected: function () {
                        return DpCategoryService.getSelectedToType(type.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, categories, selected) {

                    $scope.oryg = type;
                    $scope.form = {};
                    //$scope.form = angular.copy(group);

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


                        DpCategoryService.setSelectedToType(type.ID, $scope.form.categories).then(function (data) {

                            var result = [];

                            var gIndex = _.findIndex($scope.types, {
                                'ID': type.ID
                            });

                            if (gIndex > -1) {
                                _.each(data, function (catID) {

                                    var cIndex = _.findIndex($scope.categories, {
                                        'ID': catID
                                    });
                                    if (cIndex > -1) {
                                        result.push($scope.categories[cIndex]);
                                    } else {
                                        _.each($scope.categories, function (cat, cIndex) {
                                            var chCat = _.findWhere(cat.childs, {
                                                'ID': catID
                                            });

                                            if (angular.isDefined(chCat)) {
                                                result.push(chCat);
                                            }
                                        });
                                    }

                                });

                                if (!angular.isDefined($scope.types[gIndex].categories)) {
                                    $scope.types[gIndex].categories = [];
                                }
                                $scope.types[gIndex].categories = _.pluck(result, 'langs');
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

        $scope.copy = function(type) {
            PsTypeService.copy(type.ID).then(function(data) {
                if( data.response ) {
                    Notification.success($filter('translate')('copied_successful'));
                    $scope.refreshTypes();
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });
        };

        $scope.saveQuestionOnly = function (isQuestionOnly, typeID) {
            PsTypeService.setQuestionOnly(currentGroupID, typeID, isQuestionOnly).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('updated'));
                    $scope.refreshTypes();
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error(data.error);
            });
        };

        $scope.saveUseAlternatives = function (useAlternatives, typeID) {
            PsTypeService.setUseAternatives(currentGroupID, typeID, useAlternatives).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('updated'));
                    $scope.refreshTypes();
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error(data.error);
            });
        };

        $scope.onPriceClick = function (priceListID) {
            $scope.selectedPriceListID = priceListID;
            loadMargins()
        }

        $scope.onNatureClick = function (natureID) {
            $scope.selectedNatureID = natureID;
            loadMargins()
        }

        function loadMargins() {
            if (!$scope.selectedPriceListID || !$scope.selectedNatureID) {
                return;
            }
            MarginsService.get($scope.selectedPriceListID, $scope.selectedNatureID, currentGroupID).then(function (data) {
                $scope.margins = data;
            });
        }

        $scope.addMargin = function () {
            var data = _.clone($scope.marginForm);
            data.priceTypeID = $scope.selectedPriceListID;
            data.natureID = $scope.selectedNatureID;
            data.groupID = currentGroupID;
            MarginsService.add(data).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                    $scope.marginForm = {};
                    loadMargins()
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (error) {
                Notification.error($filter('translate')('error'));
            })
        }

        $scope.editMarginBegin = function (margin) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-margin.html',
                controller: function ($scope, $modalInstance) {
                    $scope.marginForm = _.clone(margin);
                    $scope.save = function () {
                        MarginsService.edit(margin.ID, $scope.marginForm).then(function (data) {
                            if (data.response) {
                                Notification.success($filter('translate')('success'));
                                $modalInstance.close();
                                loadMargins();
                            } else {
                                Notification.error($filter('translate')('error'));
                            }

                        }, function (error) {
                            Notification.error($filter('translate')('error'));
                        });

                    }

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        }

        $scope.removeMargin = function (marginID) {
            MarginsService.removeMargin(marginID).then(function (data) {
                    if (data.response) {
                        Notification.success($filter('translate')('success'));
                        loadMargins()
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                },
                function (error) {
                    Notification.error($filter('translate')('error'));
                })
        }
    });
