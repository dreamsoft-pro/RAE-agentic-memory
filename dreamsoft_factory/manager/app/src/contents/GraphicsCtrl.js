'use strict';
angular.module('digitalprint.app')
    .controller('contents.GraphicsCtrl', function ($scope, $filter, $cacheFactory, RouteService, ContentService,
                                                   UploadService, HomepageBannerService, TypeDescriptionsService,
                                                   ModelIconsService, Notification, $config, $modal, FileUploader,
                                                   SettingService ) {
        var uploader;
        var uploaderModels;
        var uploaderFavicon;
        var companyID = $scope.companyID = $scope.currentDomain.companyID;

        $scope.modelsFiles = [];
        $scope.thumbFiles = [];
        $scope.selectedFiles = [];
        $scope.STATIC_URL = $config.STATIC_URL;
        var settings = new SettingService('bannerSlider');

        $scope.sliderForm = {
            'sliderAutoSlide': {
                value: 0
            },
            'sliderTransition': {
                value: ''
            }
        };

        $scope.sliderTransitions = {
            'slide': {
                value: 'slide'
            },
            'zoom': {
                value: 'zoom'
            },
            'hexagon': {
                value: 'hexagon'
            },
            'fadeAndSlide': {
                value: 'fadeAndSlide'
            },
            'none': {
                value: 'none'
            }
        };

        function init() {

            $scope.thumbLogo = [];
            $scope.logoPath = $config.STATIC_URL + 'uploadedFiles/' + companyID + '/logos/' +  $scope.currentDomain.ID + '/logo';
            $scope.modelFilePath = $config.STATIC_URL + 'uploadedFiles/' + companyID + '/modelsIcons/';

            uploader = $scope.uploader = new FileUploader({
                'url': UploadService.getLogoUploadUrl(),
                'formData': [{domainID: $scope.currentDomain.ID}]
            });

            uploader.filters.push({
                name: 'imageFilter',
                fn: function (item /*{File|FileLikeObject}*/, options) {
                    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                    var checkType = '|jpg|png|jpeg|webp|bmp|gif|svg|svg+xml|'.indexOf(type) !== -1;
                    if (!checkType) {
                        Notification.warning(
                            $filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, '')
                        );
                    }
                    return checkType;
                }
            });

            uploaderModels = $scope.uploaderModels = new FileUploader({
                'url': UploadService.getModelIconsUploadUrl()
            });

            uploaderModels.filters.push({
                name: 'imageFilter',
                fn: function (item /*{File|FileLikeObject}*/, options) {
                    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                    var checkType = '|png|'.indexOf(type) !== -1;
                    if (!checkType) {
                        Notification.warning($filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, ''));
                    }
                    return checkType;
                }
            });

            uploaderFavicon = $scope.uploaderFavicon = new FileUploader({
                'url': UploadService.getFaviconUploadUrl()
            });

            uploaderFavicon.filters.push({
                name: 'imageFilter',
                fn: function (item /*{File|FileLikeObject}*/, options) {
                    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                    var checkType = '|png|ico|'.indexOf(type) !== -1;
                    if (!checkType) {
                        Notification.warning($filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, ''));
                    }
                    return checkType;
                }
            });

            ModelIconsService.getAll().then(function (data) {
                $scope.modelsExtensions = data;
            });
            UploadService.getModelFiles().then(function (data) {
                $scope.modelsFiles = data;
                $scope.modelFilePath = $config.STATIC_URL + 'uploadedFiles/' + companyID + '/modelsIcons/';
            });

            TypeDescriptionsService.getFiles().then(function (data) {
                $scope.thumbFiles = data;
            });

            HomepageBannerService.getAll().then(function (data) {
                $scope.selectedFiles = data;
            });

            settings.setModule('bannerSlider');
            settings.getAll().then(function (data) {
                $scope.sliderForm = _.merge($scope.sliderForm, data);
            });

        }

        $scope.addLogo = function () {


            $scope.uploader.uploadAll();
            uploader.onSuccessItem = function (fileItem, response, status, headers) {
                $scope.logoPath = $config.STATIC_URL + 'uploadedFiles/' + companyID + '/logos/' +  $scope.currentDomain.ID + '/logo' + '?random' + Math.floor((Math.random() * 100) + 1);
            };

        };

        $scope.addModelsIcon = function () {

            uploaderModels.queue[0].formData.push({ext: $scope.form.modelsExtensions});
            uploaderModels.uploadAll();
            uploaderModels.onCompleteAll = function () {
                uploaderModels.clearQueue();
                uploaderModels.progress = 0;
                var idx = _.findIndex($scope.modelsFiles, {
                    ext: $scope.form.modelsExtensions
                });
                if (idx > -1) {
                    $scope.modelsFiles[idx] = {
                        'name': $scope.form.modelsExtensions + '.png?random' + Math.floor((Math.random() * 100) + 1),
                        'ext': $scope.form.modelsExtensions
                    }
                } else {
                    $scope.modelsFiles.push({
                        'name': $scope.form.modelsExtensions + '.png',
                        'ext': $scope.form.modelsExtensions
                    });
                }
            };
        };

        $scope.addBanerPic = function (elem) {
            var idx = _.findIndex($scope.selectedFiles, {
                ID: elem.ID
            });
            if (idx > -1) {
                console.log('duplicate');
            } else {
                $scope.selectedFiles.push(elem);

            }
        };

        $scope.removeBanerFile = function (fileID) {
            var idx = _.findIndex($scope.selectedFiles, {
                ID: fileID
            });
            $scope.selectedFiles.splice(idx, 1);
        };

        $scope.addLinkToBanner = function (fileID) {

            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/add-link-to-banner.html',
                scope: $scope,
                controller: function ($scope, $modalInstance, $filter, Notification) {

                    var idx = _.findIndex($scope.selectedFiles, {
                        ID: fileID
                    });
                    var pathImg = _.find($scope.selectedFiles, function (sf) {
                        return sf.ID == fileID
                    });
                    $scope.linkToBannerImg = $config.STATIC_URL + 'uploadedFiles/' + companyID + '/' + pathImg.path;
                    $scope.currentLink = $scope.selectedFiles[idx].link;

                    $scope.save = function () {

                        if ($scope.selectedFiles[idx].link = $scope.form.bannerLink) {
                            $modalInstance.close();
                        } else {
                            Notification.error($filter('translate')('error'));
                        }

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }

            });
        };

        $scope.uploadBannerFiles = function () {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/uploader.html',
                scope: $scope,
                backdrop: 'static',
                keyboard: false,
                controller: function ($scope, $modalInstance, $filter, Notification) {
                    var uploader = $scope.uploader = new FileUploader({
                        'url': TypeDescriptionsService.getUploadUrl()
                    });

                    uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item /*{File|FileLikeObject}*/, options) {
                            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                            var checkType = '|jpg|png|jpeg|webp|bmp|gif|svg|svg+xml|'.indexOf(type) !== -1;
                            if (!checkType) {
                                Notification.warning($filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, ''));
                            }
                            return checkType;
                        }
                    });

                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                        if( response.response ) {
                            $scope.thumbFiles.push(response.item);
                        } else {
                            Notification.error($filter('translate')('error'));
                        }
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

        $scope.savePictures = function (currentDescID) {
            var filesData = {};
            filesData.files = $scope.selectedFiles;
            HomepageBannerService.add(filesData).then(function (data) {
                Notification.success($filter('translate')('success'));
            });
        };

        $scope.removeFile = function(file) {
            TypeDescriptionsService.removeDescriptionFile(file.ID).then(function(data) {
                if( data.response ) {
                    console.log($scope.thumbFiles, data);
                    var idx = _.findIndex($scope.thumbFiles, {
                        ID: data.item.ID
                    });
                    $scope.thumbFiles.splice(idx, 1);
                    Notification.success($filter('translate')('deleted_successful'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });
        };

        $scope.saveSliderOptions = function() {

            settings.save($scope.sliderForm).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        init();

    });