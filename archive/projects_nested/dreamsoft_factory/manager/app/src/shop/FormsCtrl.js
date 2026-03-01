/**
 * Created by Rafał on 19-07-2017.
 */
angular.module('digitalprint.app')
    .controller('shop.FormsCtrl', function ($scope, $filter, Notification, $modal,
                                            DpStatusService, SettingService) {

        var settings = new SettingService('forms');

        $scope.defaultForm = {};
        $scope.forms = [];

        function refresh() {
            $scope.forms = [];

            settings.getAll().then(function (data) {
                _.each(data, function( value, key ) {
                    value.key = key;
                    $scope.forms.push( value );
                });
            });
        }


        $scope.saveForm = function () {
            settings.setModule('forms');
            var saveData = {};
            saveData[$scope.form.key] = {};
            saveData[$scope.form.key].value = $scope.form.recipients;
            settings.save(saveData).then(function (data) {
                refresh();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (form) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-form.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = form;

                    $scope.save = function() {
                        var saveData = {};
                        saveData[form.key] = {};
                        saveData[form.key] = {'value': $scope.form.value};
                        settings.setModule('forms');
                        settings.save(saveData).then(function (data) {
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.delete = function(form) {
            settings.setModule('forms');
            settings.delete(form.key).then( function( removeSettings ) {
                if( removeSettings.response === true ) {
                    refresh();
                    Notification.success($filter('translate')('success'));
                }
            });

        };

        function init() {
            refresh();
        }

        init();

    });