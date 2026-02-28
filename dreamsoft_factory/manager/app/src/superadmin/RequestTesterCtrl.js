angular.module('digitalprint.app')
    .controller('superadmin.RequestTesterCtrl', function (localStorageService, $rootScope, $cookieStore,
                                                          AuthDataService, Upload, $scope, $http, $config,
                                                          Notification, $filter) {

        $scope.form = {};
        $scope.shortcuts = [
            {
                ID: 1,
                value: 'test/executeToAllDb',
                method: 'POST'
            }
        ];

        $scope.requestMethods = [
            {
                method: 'GET'
            },
            {
                method: 'POST'
            },
            {
                method: 'PUT'
            },
            {
                method: 'PATCH'
            },
            {
                method: 'DELETE'
            }
        ];

        $scope.form.parameters = [];
        $scope.form.fileParams = [];

        $scope.addParameter = function () {

            $scope.form.parameters.push({
                key: null,
                value: null
            });

        };

        $scope.upload = function (files, name) {
            console.log(files);
            if (files && files.length) {
                _.each(files, function (file) {
                    Upload.upload({
                        url: $config.API_URL + $scope.form.request,
                        fileFormDataName: name,
                        file: file
                    }).progress(function (evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                    }).success(function (data, status, headers, config) {
                        console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
                    }).error(function (data, status, headers, config) {
                        console.log('error status' + status);
                    });
                });
            }
        };

        $scope.addFileParam = function () {
            $scope.form.fileParams.push({
                key: null,
                uploader: null
            });

        };

        $scope.doRequest = function () {
            console.log("doRequest", $scope.form);

            var resource = $scope.form.request;

            var requestData = {};
            _.each($scope.form.parameters, function (item, i) {
                console.log(item);
                requestData[item.key] = item.value;
            });

            if ($scope.form.fileParams.length) {
                console.log($scope.form.fileParams);
                _.each($scope.form.fileParams, function (fileParam) {
                    $scope.upload(fileParam.uploader, fileParam.key)
                });
                return true;
            }

            $http({
                url: $config.API_URL + resource,
                method: $scope.form.requestMethod,
                data: requestData
            }).success(function (data) {
                Notification.success("Request ok");
                console.log(data);
                $scope.response = data;
            }).error(function (data) {
                Notification.error("Request error");
                console.log(data);
                $scope.response = data;
            });

        };

        $scope.updateTest = function () {
            var resource = 'ssh/frameworkTest';
            $http({
                url: $config.API_URL + resource,
                method: 'GET'
            }).success(function (data) {
                console.log(data);
                Notification.success("Ok");
                $scope.updateInfo = data[0] + data[1];

            }).error(function (data) {
                console.log(data);
                Notification.error("Error");
            });
        };

        $scope.updateProduction = function () {
            var resource = 'ssh/framework';
            $http({
                url: $config.API_URL + resource,
                method: 'GET'
            }).success(function (data) {
                console.log(data);
                Notification.success("Ok");
                $scope.updateInfo = data[0] + data[1];

            }).error(function (data) {
                console.log(data);
                Notification.error("Error");
            });
        };

        $scope.initPerms = function () {
            var resource = 'initPerms';
            $http({
                url: $config.API_URL + resource,
                method: 'GET'
            }).success(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error("Error");
                }
            }).error(function (data) {
                console.log(data);
                Notification.error("Error");
            });
        };

        $scope.copyPerms = function () {
            var toCompanyID = '';
            var resource = 'copyPerms';
            if ($scope.form.toCompanyID > 0) {
                toCompanyID = '?toCompanyID=' + $scope.form.toCompanyID;
            }

            $http({
                url: $config.API_URL + resource + toCompanyID,
                method: 'GET'
            }).success(function (data) {
                console.log(data);
                if (data.response) {
                    Notification.success("Skopiowano prawa dostępu");
                } else {
                    Notification.error("Error");
                }
            }).error(function (data) {
                console.log(data);
                Notification.error("Error");
            });
        };

        $scope.copyTemplate = function () {
            var dataParams = {};

            if (!(parseInt($scope.form.templateID) > 0)) {
                Notification.info("Wpisz ID szablonu");
                return;
            }

            dataParams.templateID = $scope.form.templateID;

            $http({
                url: $config.API_URL + 'test/updateTemplate',
                method: 'PATCH',
                data: dataParams
            }).success(function (data) {
                console.log(data);
                if (data.response) {
                    Notification.success("Nadpisano szablony");
                } else {
                    Notification.error("Error");
                }
            }).error(function (data) {
                console.log(data);
                Notification.error("Error");
            });
        };

        $scope.getShortcut = function( ID ) {
            var shortcutIdx = _.findIndex($scope.shortcuts, {ID: ID});
            if( shortcutIdx > -1 ) {
                $scope.form.request = $scope.shortcuts[shortcutIdx].value;
                $scope.form.requestMethod = $scope.shortcuts[shortcutIdx].method;
            }
        };

    });