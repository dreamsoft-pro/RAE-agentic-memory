angular.module('digitalprint.app')
    .controller('superadmin.ImportUsersCtrl', function ($scope, FileUploader, Notification, $filter, $config) {

        $scope.importTypes = [
            'default',
            'delivery',
            'invoice'
        ];

        $scope.import = {};

        $scope.import.type = 'default';

        $scope.uploader = new FileUploader({
            url: $config.API_URL + ['test', 'importUsers'].join('/'),
            autoUpload: false,
            queueLimit: 1
        });

        $scope.uploader.onSuccessItem = function (item, data) {
            if (data.response) {
                Notification.success(Notification.success($filter('translate')('success')));
            } else {
                Notification.error(Notification.error($filter('translate')('error')));
            }
        };

        $scope.importUsers = function() {

            var file = $scope.uploader.queue[0];

            $scope.uploader.data = {};

            file.formData = [{
                'type': $scope.import.type
            }];

            $scope.uploader.uploadItem(file);

        };


    });