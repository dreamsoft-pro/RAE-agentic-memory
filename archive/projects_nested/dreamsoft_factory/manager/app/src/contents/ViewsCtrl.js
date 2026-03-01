angular.module('digitalprint.app')
    .controller('contents.ViewsCtrl', function ($q, $scope, $filter, $modal, $stateParams, currentRoot, Notification, ViewService, TemplateService) {

        $scope.currentRoot = currentRoot;
        var currentRouteID = $scope.routeID = parseInt($stateParams.routeID);

        var ViewServiceObject = new ViewService(currentRouteID);

        var viewID;

        var variables;

        $scope.sortChange = false;
        $scope.sortableOptions = {
            stop: function (e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };

        $scope.refreshViews = function () {
            ViewServiceObject.getAll().then(function (data) {
                $scope.sortChange = false;
                $scope.views = data;

                Notification.success($filter('translate')('success'));
            }, function (data) {
            });
        };

        $scope.makeViewReplace = function (view) {
            ViewServiceObject.makeViewReplace(view.ID).then(function (data) {
                $scope.viewReplaced = data;
                var idx = _.findIndex($scope.views, {ID: view.ID});
                if (idx > -1) {
                    // $scope.views[idx] = $scope.viewReplaced;
                    $scope.views.splice(idx, 1);
                    $scope.views.splice(idx, 0, $scope.viewReplaced.item);
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.sortCancel = function () {
            $scope.refreshViews();
        };

        $scope.sortSave = function () {
            var orders = [];
            _.each($scope.views, function (elem) {
                orders.push(elem.ID);
            });

            ViewServiceObject.sort(orders).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        function getViews() {
            var def = $q.defer();

            ViewServiceObject.getAll().then(function (data) {
                $scope.views = data;
            }, function (data) {
                def.reject(data);
                Notification.error($filter('translate')('error'));
            });

            return def.promise;
        }

        getViews();

        function getTemplates() {
            var def = $q.defer();

            TemplateService.getAll().then(function (data) {
                prepareSelectGroups(data).then(function (templates) {
                    $scope.templates = templates;
                });
            }, function (data) {
                def.reject(data);
                Notification.error($filter('translate')('error'));
            });

            return def.promise;
        }

        function prepareSelectGroups(templates) {

            var def = $q.defer();

            var result = [];
            var templatesLength = templates.length;
            _.each(templates, function (template, index) {
                template.ownName = $filter('translate')(template.ownName);
                result.push(template);
                if (index === templatesLength - 1) {
                    def.resolve(result);
                }
            });

            return def.promise;
        }

        getTemplates();

        function getReplaceViews() {
            var def = $q.defer();

            ViewServiceObject.getReplaceViews().then(function (data) {
                $scope.replaces = data;
            }, function (data) {
                def.reject(data);
                Notification.error($filter('translate')('error'));
            });

            return def.promise;
        }

        getReplaceViews();

        $scope.add = function () {
            ViewServiceObject.add($scope.form).then(function (data) {
                $scope.form = {};
                $scope.views.push(data.item);
                getViews();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('success'));
            });
        };

        $scope.edit = function (view) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-view.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

                    $scope.view = view;
                    $scope.form = _.clone(view, true);

                    $scope.ok = function () {

                        ViewServiceObject.edit($scope.form).then(function (data) {
                            view = _.extend(view, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (view) {

            ViewServiceObject.remove(view.ID).then(function (data) {
                var idx = _.findIndex($scope.views, {
                    ID: view.ID
                });
                if (idx > -1) {
                    $scope.views.splice(idx, 1);
                }
                $scope.refreshViews();

                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };


        $scope.variable = function (view) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/variable.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    variables: function () {
                        return ViewServiceObject.getAllVariables(view.ID).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                },
                controller: function ($modalInstance, $scope, variables) {
                    $scope.form = {};
                    $scope.view = view;
                    $scope.form.viewID = view.ID;
                    $scope.variables = variables;

                    $scope.add = function () {
                        ViewServiceObject.addVariable($scope.form, viewID).then(function (data) {
                            $scope.variables.push(data.item);
                            $scope.form = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
                        });
                    };

                    $scope.remove = function (variable) {

                        ViewServiceObject.removeVariable(variable.ID).then(function (data) {

                            var idx = _.findIndex($scope.variables, {
                                ID: variable.ID
                            });
                            if (idx > -1) {
                                $scope.variables.splice(idx, 1);
                            }
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }

                }
            });
        };

        $scope.template = function (view) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-template.html',
                scope: $scope,
                resolve: {
                    templates: function () {
                        return TemplateService.getAll().then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                },
                controller: function ($modalInstance, $scope, templates) {

                    prepareSelectGroups(templates).then(function (templates) {
                        $scope.templates = templates;
                    });

                    $scope.form = _.clone(view);
                    $scope.form.templateIndex = _.findIndex($scope.templates, {
                        ID: $scope.form.templateID,
                        own: view.own
                    });

                    $scope.add = function () {

                        if( $scope.templates[$scope.form.templateIndex] !== undefined ) {

                            $scope.form.template = $scope.templates[$scope.form.templateIndex];
                            $scope.form.templateID = $scope.templates[$scope.form.templateIndex].ID;


                            if ($scope.form.template.own) {
                                $scope.form.templateRoot = 2;
                            } else {
                                $scope.form.templateRoot = 1;
                            }

                        } else {
                            $scope.form.templateID = null;
                        }

                        ViewServiceObject.addViewTemplate($scope.form).then(function (data) {
                            view = _.extend(view, $scope.form);
                            if (data.response) {
                                if (data.item) {
                                    var viewIdx = _.findIndex($scope.views, {ID: data.item.ID});
                                    if (viewIdx > -1) {
                                        $scope.views[viewIdx] = data.item;
                                    }
                                }
                                $modalInstance.close();
                                Notification.success($filter('translate')('success'));
                            }
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.addVariable = function () {

            ViewServiceObject.addVariable($scope.form).then(function (data) {
                $scope.variables.push(data.item);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.editVariable = function (variable) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-variable.html',
                scope: $scope,

                controller: function ($scope, $modalInstance) {
                    $scope.variable = _.clone(variable);
                    $scope.form = _.clone(variable);

                    $scope.save = function () {
                        ViewServiceObject.editVariable($scope.form).then(function (data) {
                            variable = _.extend(variable, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.removeVariable = function (variable) {

            ViewServiceObject.removeVariable(variable.ID).then(function (data) {

                var idx = _.findIndex($scope.variable, {
                    ID: variable.ID
                });
                $scope.variables.splice(idx, 1);
                Notification.success($filter('translate')('success'));

            }, function (data) {

                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));

            });
        };

        // End of Variables

    });