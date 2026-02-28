'use strict';
angular.module('digitalprint.app')
    .controller('contents.TemplateVariablesCtrl', function ($q, $rootScope, $scope, $filter, $modal, Notification,
                                                            TemplateVariablesService, StaticContentService) {
        function loadAll() {
            $q.all([TemplateVariablesService.getTemplates(),
                TemplateVariablesService.getGlobalVariables(),
                TemplateVariablesService.getAll()
            ]).then(function (data) {
                $scope.templates = data[0];
                $scope.templateVariables = data[2];
                var templateNames = Object.fromEntries(data[0].map(function (item) {
                    return [item.ID, item.name]
                }));
                var global = data[0].slice();//TODO not workking
                global.forEach(function (template) {
                    template.templateName = templateNames[template.ID];
                    var variablesForTemplate = $scope.templateVariables.filter(function (variable) {//TODO root/no root
                        return variable.templateName == template.name
                    });
                    template.variables = variablesForTemplate.map(function (variable) {
                        var current = data[1].find(function (item) {
                            return item.templateVariableTypeID == variable.ID;
                        });
                        variable.valuesArray = variable.values.split('|').map(function (value) {

                            return {name: value, selected: current != undefined && current.value==value, ID: current ? current.ID : null}
                        });
                        return variable;
                    })
                });
                $scope.globalTemplateVariables = global;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        loadAll();

        $scope.templateStatic = {};
        TemplateVariablesService.getAll().then(function (variables){
            variables.forEach(function (variable) {
                StaticContentService.getContent('variables.'+variable.name).then(function(data) {
                    if(data.contents){
                        $scope.templateStatic[variable.name] = data.contents[$rootScope.currentLang.code];
                    }
                });
            });
        });

        $scope.saveVariable = function (variable, value) {
            if (value.ID) {
                TemplateVariablesService.updateAssoc(value.ID, {value:value.name}).then(function () {
                    Notification.success($filter('translate')('success'));
                    loadAll();
                }, function () {
                    Notification.error($filter('translate')('error'));
                })
            } else {
                var data = _.clone(variable);
                data.value = value.name;
                TemplateVariablesService.saveAssoc(data).then(function () {
                    Notification.success($filter('translate')('success'));
                    loadAll();
                }, function () {
                    Notification.error($filter('translate')('error'));
                })
            }

        }
        $scope.form = {};
        $scope.add = function () {
            TemplateVariablesService.add(this.form).then(function () {
                Notification.success($filter('translate')('success'));
                loadAll();
            }, function () {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (templateVariableType) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-template-variable-type.html',
                scope: $scope,

                controller: ['$scope','$modalInstance','TemplateVariablesService',
                    function ($scope, $modalInstance, TemplateVariablesService) {
                    $scope.form = _.clone(templateVariableType);

                    $scope.ok = function () {
                        var data = _.clone(this.form);
                        TemplateVariablesService.edit(data.ID, data).then(function (data) {
                            $modalInstance.close();
                            loadAll();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error') + ' ' + data.info)
                        });
                    }
                }]
            });
        };

        $scope.remove = function (item) {
            TemplateVariablesService.remove(item.ID).then(function () {
                Notification.success($filter('translate')('success'));
                loadAll();
            }, function () {
                Notification.error($filter('translate')('error'));
            });
        }
    });
