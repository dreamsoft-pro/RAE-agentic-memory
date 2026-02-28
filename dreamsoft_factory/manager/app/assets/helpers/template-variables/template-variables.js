angular.module('digitalprint.helpers')
    .directive('templateVariables', [
        function () {
            var assocID,role;
            return {
                restrict: 'E',
                replace: true,
                template: '<button class="btn blue-hoki btn-xs"\n' +
                    '        ng-click="launchModal();" tooltip="{{ \'template_variables\' | translate }}">\n' +
                    '    <i class="fa fa-tv"></i>\n' +
                    '</button>',
                link: function (scope, element, attr) {
                    assocID = attr.associd;
                    role = attr.role;
                },
                controller: function ($scope, $q, $filter, $config, $modal, $location,
                                      TemplateVariablesService, Notification) {
                    $scope.launchModal = function () {
                        function languageList(items, langCode) {
                            items = _.filter(items, function (item) {
                                return item.lang != langCode
                            });
                            return _.map(items, function (item) {
                                return {ID: item.ID, name: item.slug}
                            })
                        }

                        var modalInstance = $modal.open({
                            templateUrl: 'views/modalboxes/template-variables.html',
                            controller: ['$modalInstance', '$scope', '$rootScope', '$filter',
                                'TemplateVariablesService', 'Notification', '$config',
                                function ($modalInstance, $scope, $rootScope, $filter, TemplateVariablesService,
                                          Notification, $config) {
                                    $scope.settings = {};
                                    function loadItemVariables(){
                                        TemplateVariablesService.getForRange(role, assocID).then(function (data) {
                                            $scope.templateVariables = data;
                                        });
                                    }
                                    loadItemVariables();
                                    $scope.add = function () {
                                        TemplateVariablesService.saveAssoc($scope.settings).then(function () {
                                            $modalInstance.close();
                                        }, function () {
                                            Notification.error($filter('translate')('error'));
                                        })
                                    };
                                    $scope.cancel = function () {
                                        $modalInstance.close();
                                    }
                                }]
                        });

                    }
                }
            }
        }]);
