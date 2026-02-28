angular.module('digitalprint.app')
    .controller('shop.LangSettingsCtrl', function ($scope, $rootScope, $filter, $modal,
                                                   LangSettingsService, LangSettingsRootService, Notification) {

        $scope.form = {};
        $scope.activeRootLanguages = [];

        LangSettingsService.getAll().then(function (data) {
            $scope.langlist = data;
        });

        LangSettingsRootService.getAll().then( function(data) {
            $scope.activeRootLanguages = [];
            _.each(data, function(one) {
                 if( one.active ) {
                     $scope.activeRootLanguages.push(one);
                 }
            });
        });

        $scope.refresh = function () {
            LangSettingsService.getAll(true).then(function (data) {
                $scope.langlist = data;
            });
            LangSettingsRootService.getAll().then( function(data) {
                $scope.activeRootLanguages = [];
                _.each(data, function(one) {
                    if( one.active ) {
                        $scope.activeRootLanguages.push(one);
                    }
                });
            });
        };

        $scope.reset = function () {
            $scope.form.code = 'en';
        };
        $scope.reset();

        $scope.add = function () {

            if( !$scope.form.code ) {
                Notification.error($filter('translate')('select_language'));
                return;
            }

            LangSettingsService.create($scope.form).then(function (data) {
                $scope.refresh();
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.edit = function (lang) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-lang-settings.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = $scope.lang = _.clone(lang);

                    $scope.ok = function () {
                        var formData = _.clone($scope.form);
                        formData.active = formData.active ? 1 : 0;
                        formData.default = formData.default ? 1 : 0;
                        LangSettingsService.update(formData).then(function (data) {
                            $scope.refresh();
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };


        $scope.remove = function (id) {

            var idx = _.findIndex($scope.langlist, {
                ID: id
            });

            LangSettingsService.remove(id).then(function () {
                $scope.langlist.splice(idx, 1);
                Notification.success($filter('translate')('success'));
            });

        };

    });
