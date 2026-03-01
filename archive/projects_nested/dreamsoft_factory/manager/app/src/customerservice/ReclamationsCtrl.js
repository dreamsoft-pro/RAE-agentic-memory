/**
 * Created by Rafał on 08-09-2017.
 */
angular.module('digitalprint.app')
    .controller('customerservice.ReclamationsCtrl', function ($scope, $rootScope, ApiCollection, ReclamationStatusService,
                                                              $modal, MainWidgetService, ReclamationService, socket,
                                                              localStorageService, $filter, Notification, DpAddressService,
                                                              $timeout, FileUploader, $config) {

        $scope.statuses = [];

        $scope.showRows = 25;
        $scope.reclamationsConfig = {
            count: 'dp_reclamations/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.reclamationsCtrl.items = data;
            }
        };

        var accessTokenName = $config.ACCESS_TOKEN_NAME;

        var updateTableTimeout = null;

        $scope.reclamationsCtrl = new ApiCollection('dp_reclamations', $scope.reclamationsConfig);
        $scope.reclamationsCtrl.get();


        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.reclamationsCtrl.get();
            }, 1000);
        };

        $scope.files = function (reclamation) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/reclamation-files.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope) {
                    $scope.files = reclamation.files;

                    var header = {};
                    header[accessTokenName] = localStorageService.get(accessTokenName);

                    $scope.uploader = new FileUploader({
                        'url': ReclamationService.getUploadUrl(reclamation.ID),
                        headers: header,
                        'autoUpload': false
                    });

                    $scope.uploader.onProgressAll = function (progress) {
                        $scope.uploadProgress = progress;
                    };

                    $scope.uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item, options) {
                            var itemName = item.name.split('.');
                            var lastItem = itemName.pop();
                            var possibleExtensions = ['jpg', 'jpeg','webp'];

                            if (possibleExtensions.indexOf(lastItem) > -1) {
                                return true;
                            }
                            Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                            return false;
                        }
                    });

                    $scope.upload = function () {
                        $scope.uploader.uploadAll();
                        $scope.uploader.onCompleteAll = function () {

                            ReclamationService.getFiles(reclamation.ID).then(function(filesData) {
                                var idx = _.findIndex($scope.reclamations, {ID: reclamation.ID});
                                if( idx > -1 ) {
                                    $scope.reclamations[idx].files = filesData;
                                }
                                $scope.selectedReclamation = null;
                                $scope.uploader.clearQueue();
                                $scope.uploadProgress = 0;
                                $scope.files = filesData;
                                Notification.success($filter('translate')('file_uploaded'));
                            });

                        }
                    };

                    $scope.cancelUpload = function() {
                        $scope.uploader.clearQueue();
                    };
                }
            });
        };

        function getMessages(scope, reclamationID) {
            ReclamationService.getMessages(reclamationID).then(function(data) {
                scope.messages = data;
            });
        }

        $scope.messages = function(reclamation) {

            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/reclamation-messages.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance, $config) {

                    $scope.reclamation = reclamation;
                    $scope.messages = [];

                    reclamation.unreadMessages = 0;

                    socket.emit('onReclamation', {'reclamationID': reclamation.ID});

                    getMessages($scope, reclamation.ID);

                    $scope.send = function() {

                        if( this.form === undefined || this.form.message === undefined
                            || this.form.message.length === 0 ) {
                            Notification.error($filter('translate')('fill_form_to_contact'));
                            return;
                        }

                        socket.emit('addAdminMessage', {
                            'reclamationID': reclamation.ID,
                            'message': this.form.message,
                            'accessToken': localStorageService.get(accessTokenName),
                            'companyID': $scope.currentDomain.companyID
                        });
                    };

                    socket.on('messageSaved', function(data) {
                        if(data.ID !== undefined) {
                            if( $scope.form && data.isAdmin === 1 ) {
                                $scope.form.message = '';
                                var params = {
                                    content: data.content,
                                    reclamationID: data.reclamationID,
                                    orderMessageID: data.ID
                                };
                                if( $scope.form.sendAlsoByEmail ) {
                                    ReclamationService.sendEmail(params).then(function(sendData) {
                                        if(sendData.response) {
                                            Notification.success($filter('translate')('email_sended'));
                                        } else {
                                            Notification.error($filter('translate')('error'));
                                        }
                                    }, function(errorData) {
                                        Notification.error($filter('translate')(errorData.info));
                                    });
                                    $scope.form.sendAlsoByEmail = false;
                                }

                            }
                            getMessages($scope, reclamation.ID);
                        }
                    });

                }
            });
        };

        $scope.defaultAddress = function( reclamationUser ) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/default-address.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance, $config) {

                    $scope.address = {};

                    DpAddressService.getDefaultAddress(reclamationUser.ID, 1).then( function(data) {
                       $scope.address = data.address;
                    });

                }
            });
        };

        $scope.changeStatus = function (reclamation) {

            ReclamationService.put(reclamation.ID, {
                statusID: reclamation.statusID
            }).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.formatSizeUnits = function(file){
            return MainWidgetService.formatSizeUnits(file.size);
        };

        function init() {
            ReclamationStatusService.getAll().then(function (data) {
                $scope.statuses = data;


            });

            $rootScope.$emit('Reclamations:unreadMessages', 0);

            socket.emit('onReclamationsAdminPanel', {'admin': true});

            socket.on('newMessage', function( newMessage ) {
                var reclamationIdx = _.findIndex($scope.reclamationsCtrl.items, {ID: newMessage.reclamationID});
                if( reclamationIdx > -1 ) {
                    if( $scope.reclamationsCtrl.items[reclamationIdx].unreadMessages === undefined ) {
                        $scope.reclamationsCtrl.items[reclamationIdx].unreadMessages = 1;
                    } else {
                        $scope.reclamationsCtrl.items[reclamationIdx].unreadMessages++;
                    }
                }
            });
        }

        init();
    });