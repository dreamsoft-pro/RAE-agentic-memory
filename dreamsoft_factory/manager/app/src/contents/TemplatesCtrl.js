'use strict';
angular.module('digitalprint.app')
    .controller('contents.TemplatesCtrl', function ($q, $scope, $filter, $modal, Notification,
                                                    TemplateRootService, TemplateService) {

        $scope.templates = [];

        $scope.getAllTemplates = function(){
            TemplateService.getAll().then(function (data) {
                $scope.templates = data;
            });
        }
        $scope.getAllTemplates();

        $scope.add = function () {
            TemplateService.add($scope.form).then(function (data) {
                $scope.templates.push(data.item);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.edit = function (template) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-template-props.html',
                scope: $scope,

                controller: function ($scope, $modalInstance) {
                    $scope.template = _.clone(template);
                    $scope.form = _.clone(template);

                    $scope.ok = function () {
                        var theService = template.own === true ? TemplateService : TemplateRootService;
                        theService.edit($scope.form).then(function (data) {
                            template = _.extend(template, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error') + ' ' + data.info)
                        });
                    }
                }
            });
        };

        $scope.changeSource = function (template) {

            if (template.own === true) {
                TemplateService.setSource({templateID: template.ID, source: template.source}).then(function (data) {
                    if (data.response) {
                        if (data.item) {
                            var templateIndex = _.findIndex($scope.templates, {ID: data.item.ID, own: true});
                            if (templateIndex > -1) {
                                $scope.templates[templateIndex] = data.item;
                            }
                        }
                        Notification.success($filter('translate')('success'));
                    }
                }, function () {
                    Notification.error($filter('translate')('error'));
                });
            } else {
                TemplateRootService.setSource({templateID: template.ID, source: template.source}).then(function (data) {
                    if (data.response) {
                        if (data.item) {
                            var templateIndex = _.findIndex($scope.templates, {ID: data.item.ID, own: false});
                            if (templateIndex > -1) {
                                $scope.templates[templateIndex] = data.item;
                            }
                        }
                        Notification.success($filter('translate')('success'));
                    }
                }, function () {
                    Notification.error($filter('translate')('error'));
                });
            }


        };

        $scope.uploadFile = function (template) {
            function updateTemplates(data, own) {
                if (data.item) {
                    var templateIndex = _.findIndex($scope.templates, {ID: data.item.ID, own: own});
                    if (templateIndex > -1) {
                        $scope.templates[templateIndex] = data.item;
                    }
                }
            }
            if (template.own === true) {
                if (template.file && template.file.length && template.source > 0) {
                    TemplateService.uploadFile(template).progress(function (evt) {
                        var progressPercentage = parseInt(100.00 * evt.loaded / evt.total);
                        template.progress = progressPercentage;
                    }).success(function (data, status, headers, config) {
                        if (!data.response) {
                            Notification.error($filter('translate')('error'));
                            return false;
                        }
                        updateTemplates(data,true)
                        template.progress = 0;
                        Notification.success($filter('translate')('success'));
                    }).error(function (data, status, headers, config) {
                        Notification.error($filter('translate')('error'));
                    });
                }
            } else {
                if (template.file && template.file.length && template.source > 0) {
                    TemplateRootService.uploadFile(template).progress(function (evt) {
                        var progressPercentage = parseInt(100.00 * evt.loaded / evt.total);
                        template.progress = progressPercentage;
                    }).success(function (data, status, headers, config) {
                        if (!data.response) {
                            Notification.error($filter('translate')('error'));
                            return false;
                        }
                        updateTemplates(data,false)
                        template.progress = 0;
                        Notification.success($filter('translate')('success'));
                    }).error(function (data, status, headers, config) {
                        Notification.error($filter('translate')('error'));
                    });
                }
            }

        };

        $scope.remove = function (template) {
            if (template.own === false) {
                return;
            }
            TemplateService.remove(template.ID).then(function (data) {

                var idx = _.findIndex($scope.templates, {
                    ID: template.ID, own: true
                });
                if (idx > -1) {
                    $scope.templates.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));

            }, function (data) {

                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));

            });
        };

        $scope.getFile = function (template) {
            if (template.own === true) {
                return TemplateService.getFile(template.ID);
            } else {
                return TemplateRootService.getFile(template.ID);
            }
        };

        $scope.removeFile = function (template) {
            if (template.source === 0) {
                return;
            }
            if (template.own === true) {
                TemplateService.removeFile(template).then(function (data) {
                    if (data.response) {
                        var idx = _.findIndex($scope.templates, {
                            ID: template.ID, own: template.own
                        });
                        if (idx > -1) {
                            $scope.templates[idx].fileExist = false;
                        }
                        Notification.success($filter('translate')('success'));
                    }
                });
            } else {
                TemplateRootService.removeFile(template).then(function (data) {
                    if (data.response) {
                        var idx = _.findIndex($scope.templates, {
                            ID: template.ID, own: template.own
                        });
                        if (idx > -1) {
                            $scope.templates[idx].fileExist = false;
                        }
                        Notification.success($filter('translate')('success'));
                    }
                });
            }
        };

    });
