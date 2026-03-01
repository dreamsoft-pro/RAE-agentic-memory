angular.module('digitalprint.app')
    .controller('superadmin.SocketTesterCtrl', function ($scope, socketService, $config, Notification) {

        $scope.newSocketForm = {};
        $scope.sockets = [];

        $scope.newSocket = function () {
            var socket = {
                port: $scope.newSocketForm.port,
                responses: [],
                listeners: []
            };
            socket.io = new socketService($scope.newSocketForm.port);
            $scope.sockets.push(socket);
        };

        $scope.emit = function (socket, eventName, data) {
            data = JSON.parse(data);
            var res = socket.io.emit(eventName, data);
            console.log(res);
        };

        $scope.on = function (socket, eventName) {
            var exist = _.findIndex(socket.listeners, {name: eventName});
            if (exist > -1) {
                Notification.error("listener exists");
                return true;
            }

            var listener = {name: eventName, responses: []};
            socket.listeners.push(listener);
            socket.io.on(eventName, function (data) {
                console.log(data);
                socket.responses.push({data: data, eventName: eventName});
            });
            Notification.success("socket on OK");
        };

        $scope.removeListener = function (socket, listener) {
            socket.io.remove(listener.name);
            var idx = socket.listeners.indexOf(listener);
            if (idx > -1) {
                socket.listeners.splice(idx, 1);
            }
        };


    });