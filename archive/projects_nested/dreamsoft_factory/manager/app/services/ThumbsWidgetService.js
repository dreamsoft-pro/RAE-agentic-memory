/**
 * Created by Rafał on 15-03-2017.
 */
angular.module('digitalprint.services')
    .factory('ThumbsWidgetService', function ( $modal, CategoryDescriptionsService, SubcategoryDescriptionsService,
                                               $filter, Notification, FileUploader ) {

        function ThumbsWidgetService(json) {
            angular.extend(this, json);
        }

        function getThumbsModal( $scope, element, service ) {

            var currentDescID = $scope.currentDescID = element.descID;
            var companyID = $scope.companyID = $scope.currentDomain.companyID;

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/uploader-thumbs.html',
                scope: $scope,
                resolve: {
                    descFiles: function () {
                        return service.getDescriptionFile(currentDescID).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, descFiles) {

                    $scope.oryg = element;
                    $scope.selectedFiles = descFiles;
                    service.getFiles().then(function (data) {
                        $scope.thumbFiles = data;
                    });

                    $scope.addPicture = function (elem, currentDescID) {
                        var idx = _.findIndex($scope.selectedFiles, {
                            ID: elem.ID
                        });
                        if (idx > -1) {
                            console.log('duplicate');
                        } else {
                            $scope.selectedFiles.push(elem);

                        }

                    };

                    uploadFile( $scope, service, 'thumbFiles' );

                    $scope.savePictures = function (currentDescID) {

                        var filesData = {};
                        filesData.files = $scope.selectedFiles;
                        filesData.descID = currentDescID;
                        service.setDescriptionFile(filesData).then(function (data) {
                            Notification.success($filter('translate')('success'));
                        });
                    };
                    $scope.removeDescFile = function (fileID) {
                        removeDescFile($scope, fileID);
                    };

                    $scope.removeFile = function(file) {
                        removeFile($scope, CategoryDescriptionsService, 'thumbFiles', file);
                    };

                    $scope.form = element;
                    $scope.save = function () {

                        service.editDescription($scope.form).then(function (data) {
                            if (data.response) {
                                element = data.item;
                                Notification.success($filter('translate')('success'));
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        },function() {
                            Notification.error($filter('translate')('error'));
                        });
                    };
                }
            });

        }

        function uploadFile( $scope, service, destination ) {

            $scope.uploadFiles = function () {
                $modal.open({
                    templateUrl: 'src/printshop/templates/modalboxes/uploader.html',
                    scope: $scope,
                    backdrop: 'static',
                    keyboard: false,
                    controller: function ($scope, $modalInstance) {
                        var uploader = $scope.uploader = new FileUploader({
                            'url': service.getUploadUrl()
                        });

                        uploader.onSuccessItem = function (fileItem, response, status, headers) {
                            addFilesToView( $scope, destination, response );
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

        }

        function removeFile($scope, service, destination, file) {
            service.removeDescriptionFile(file.ID).then(function(data) {
                if( data.response ) {
                    var idx = _.findIndex($scope[destination], {
                        ID: data.item.ID
                    });
                    if( idx > -1 ) {
                        $scope[destination].splice(idx, 1);
                    }
                    removeDescFile($scope, data.item.ID);

                    Notification.success($filter('translate')('deleted_successful'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });
        }

        function removeDescFile($scope, fileID) {
            var idx = _.findIndex($scope.selectedFiles, {
                ID: fileID
            });
            if(idx > -1) {
                $scope.selectedFiles.splice(idx, 1);
            }

        }

        function addFilesToView( $scope, destination, data ) {
            $scope[destination].push(data.item);
        }

        return {
            getThumbsModal: getThumbsModal
        };
    });