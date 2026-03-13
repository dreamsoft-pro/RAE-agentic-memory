'use strict';
angular.module('digitalprint.app')
    .controller('contents.SeoCtrl', function ($scope, $filter, $cacheFactory, $modal, ConfigService, RouteService, ContentService, Notification, MetaTagService, $config, AuthDataService, FileUploader) {

        var ContentEdit;
        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        $scope.siteMapUrl = $config.STATIC_URL + 'uploadedFiles/' + $scope.currentDomain.companyID + '/sitemap/sitemap.xml';

        function init() {
            $scope.routes = [];
            $scope.selectedRoute = null;
            $scope.refresh(true);
            $scope.routeLevels = [];
            $scope.currentSlug = null;
            $scope.lastCurrentSlug = null;
            $scope.routeBreadcrumbs = [];
            $scope.card_opt = [{
                name: $filter('translate')('twitter_summary'), code: 'twitter_summary'
            }, {
                name: $filter('translate')('twitter_summary_large_image'), code: 'twitter_summary_large_image'
            }, {
                name: $filter('translate')('empty'), code: ''
            }];
        }

        $scope.refresh = function () {
            RouteService.getAll().then(function (data) {
                $scope.routes = data;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.levelBack = function () {
            var last = $scope.routeBreadcrumbs.pop();
            $scope.currentSlug = last.slug;
            $scope.getLevel(last.slug);
        };

        $scope.getLevel = function (slug) {
            RouteService.level(slug).then(function (data) {
                $scope.routeBreadcrumbs.push({name: $scope.currentSlug, slug: $scope.currentSlug});
                $scope.currentSlug = slug;
                $scope.routes = data;
            });
        };

        $scope.selectRoute = function (route) {
            $scope.selectedRoute = route;
            $scope.currentContent = null;
            ContentEdit = new ContentService(route.ID);

            $scope.getContents().then(function (data) {
                if ($scope.contentsList.length) {
                    $scope.selectContent($scope.contentsList[0]);
                }
            });
        };

        $scope.editMetaTag = function (route) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/meta-tag-edit.html',
                size: 'lg',
                scope: $scope,
                resolve: {
                    metaTag: function () {
                        return MetaTagService.get(route.ID).then(function (data) {
                            if (data.response === false) {
                                return {};
                            } else {
                                return data;
                            }
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, metaTag) {
                    $scope.metaTag = metaTag;
                    $scope.images = {};

                    $scope.save = function () {
                        if (metaTag.ID) {
                            MetaTagService.edit($scope.metaTag, $scope).then(function (editData) {
                                if (editData.response) {

                                    $scope.metaTag = editData.item;
                                    Notification.success($filter('translate')('saved_message'));
                                    $modalInstance.close();
                                } else {
                                    Notification.error($filter('translate')('error'));
                                }
                            });
                        } else {
                            MetaTagService.add($scope.metaTag, route.ID).then(function (addData) {
                                if (addData.response) {
                                    $scope.metaTag = addData.item;
                                    Notification.success($filter('translate')('saved_message'));
                                    $modalInstance.close();
                                } else {
                                    Notification.error($filter('translate')('error'));
                                }
                            });
                        }
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };
                    $scope.uploadImage = function (image, lang, tagID) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/image-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            resolve: {
                                image: function () {
                                    return image;
                                }, lang: function () {
                                    return lang;
                                }, tagID: function () {
                                    return tagID;
                                },
                            },
                            controller: function ($scope, $modalInstance, image, lang, tagID) {
                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();
                                var uploader = $scope.uploader = new FileUploader({
                                    'url': MetaTagService.getUploadUrl(),
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
                                    formData.push({'metatagID': tagID});
                                    formData.push({'language': lang});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response) {
                                        if (response.response === true) {
                                            // ensure that lang entry exist
                                            if ($scope.$parent.metaTag.languages[response.lang]===undefined){
                                                $scope.$parent.metaTag.languages[response.lang] = {};
                                            }
                                            $scope.$parent.metaTag.languages[response.lang].imageID = response.image.ID;
                                            $scope.$parent.metaTag.images[response.image.ID] = response.image;
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
                    $scope.deleteImage = function (lang, metatag) {
                        MetaTagService.deleteImage(lang, metatag.ID).then(function (data) {
                            if (data.response) {
                                metaTag.images[metatag.languages[lang].imageID] = null;
                                metaTag.languages[lang].imageID = null;
                                Notification.success($filter('translate')('deleted_successful'));

                            }
                        });
                    };

                }


            });
        };

        $scope.refreshSiteMap = function () {
            ConfigService.generateSiteMap().then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function () {
                Notification.error($filter('translate')('error'));
            });
        };

        init();
    });