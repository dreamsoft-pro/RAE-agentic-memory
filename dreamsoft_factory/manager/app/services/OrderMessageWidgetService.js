angular.module('digitalprint.services')
    .factory('OrderMessageWidgetService', function (OrderMessageService, $modal, $filter, Notification,
                                                    AuthDataService) {

        function messagesModal(scope, order, socket, typeOfResource) {

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/order-messages.html',
                scope: scope,
                size: 'lg',
                controller: function ($scope, $modalInstance, $config) {

                    $scope.typeOfResource = typeOfResource;

                    $scope.order = order;
                    $scope.messages = [];

                    order.unreadMessages = 0;

                    socket.emit('onOrder', {'orderID': order.ID});

                    getMessages($scope, order.ID);

                    $scope.send = function () {

                        if (this.form === undefined || this.form.message === undefined
                            || this.form.message.length === 0) {
                            Notification.error($filter('translate')('fill_form_to_contact'));
                            return;
                        }

                        if (order.countMessages === undefined) {
                            order.countMessages = 1;
                        } else {
                            order.countMessages++;
                        }

                        socket.emit('order.addAdminMessage', {
                            'orderID': order.ID,
                            'message': this.form.message,
                            'accessToken': AuthDataService.getAccessToken(),
                            'companyID': $scope.currentDomain.companyID
                        });
                    };

                    socket.on('order.messageSaved', function (data) {
                        if (data.ID !== undefined) {
                            if ($scope.form && data.isAdmin === 1) {
                                var params = {
                                    content: data.content,
                                    orderID: data.orderID,
                                    orderMessageID: data.ID
                                };
                                if ($scope.form.sendAlsoByEmail) {
                                    OrderMessageService.sendEmailMessage(params).then(function (sendData) {
                                        if (sendData.response) {
                                            Notification.success($filter('translate')('email_sended'));
                                        } else {
                                            Notification.error($filter('translate')('error'));
                                        }
                                    }, function (errorData) {
                                        Notification.error($filter('translate')(errorData.info));
                                    });
                                    $scope.form.sendAlsoByEmail = false;
                                }
                                $scope.form.message = '';
                            }
                            getMessages($scope, order.ID);
                        }
                    });
                }
            });
        }

        function getMessages(scope, orderID) {
            OrderMessageService.getMessages(orderID).then(function (data) {
                scope.messages = data;
            });
        }

        return {
            messagesModal: messagesModal
        };

    });