angular.module('digitalprint.directives')
    .directive('buttonSelectAll', function () {
        return {
            restrict: 'E',
            template: '<a ng-click="selectFunction($event)" tooltip="{{ \'select_unselect_all\' | translate }}" class="buttonSelectAll"><i class="fa fa-check-square"></i></a>',
            replace: true,
            link: function (scope, elem, attrs) {
                var selectedAll = false;
                scope.selectFunction = function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    selectedAll = !selectedAll;
                    this.$parent.selectAllImpl(attrs['id'], selectedAll)
                }
            }
        }

    })
    .directive('buttonRelatedIncreases', function (PsConfigOptionService, $modal, $filter, Notification) {
        return {
            restrict: 'E',
            template: '<button class="btn" ng-click="setRelatedIncreases()">{{levelLabel+"related_increases" | translate}}<span class="badge">{{relatedIncreaseCount}}</span></button>',
            replace: true,
            scope: true,
            link: function (scope, elem, attrs) {
                var attrID = attrs['attrId'];
                var optID =scope.optID= attrs['optId'] ? attrs['optId'] : null;
                var controllerID = attrs['controllerId'] ? attrs['controllerId'] : null;

                var ConfigOptionService = new PsConfigOptionService(attrID);

                attrs.$observe('controllerId', function (value) {
                    if (value != controllerID) {
                        controllerID = value;
                        scope.getRelatedIncreasesCount();
                    }
                    updateLabel()
                })
                function updateLabel(){
                    scope.levelLabel=optID?(controllerID?'controller_':'option_'):'atrribute_'
                }
                updateLabel()
                scope.getRelatedIncreasesCount = function () {
                    ConfigOptionService.getRelatedIncreaseCount(optID, controllerID)
                        .then(function (data) {
                            scope.relatedIncreaseCount = data;
                        })
                };
                scope.getRelatedIncreasesCount();
                scope.setRelatedIncreases = function (e) {

                    $modal.open({
                        templateUrl: 'src/printshop/templates/modalboxes/increases_related.html',
                        scope: scope,
                        resolve: {
                            attributes: function () {
                                return ConfigOptionService.getAttributesForIncreases().then(function (data) {
                                    return data;
                                });
                            },
                            selected: function () {
                                return ConfigOptionService.getRelatedIncreases(optID, controllerID).then(function (data) {
                                    return data;
                                });
                            }
                        },
                        controller: function ($scope, $modalInstance, attributes, selected) {
                            $scope.attributes = _.clone(attributes, true);

                            $scope.countRelated = function (node) {
                                var count = ['attributeOptions', 'controllers'].reduce(function (count, colectionName) {
                                    if (node[colectionName]) {
                                        return node[colectionName].reduce(function (count2, item) {
                                            return count2 + (item.selected ? 1 : 0)
                                        }, 0)
                                    }
                                    return count
                                }, 0);
                                return count > 0 ? count : '';
                            };
                            _.each($scope.attributes, function (attribute, index) {

                                $scope.attributes[index].selected = _.any(selected, function (item) {
                                    return item.attrIDRelated == attribute.ID && item.optIDRelated == null && item.controllerIDRelated == null;
                                }) ? 1 : 0;

                                _.each($scope.attributes[index].attributeOptions, function (optionItem, index2) {

                                    $scope.attributes[index].attributeOptions[index2].selected = _.any(selected, function (item) {
                                        return item.attrIDRelated == attribute.ID && item.optIDRelated == optionItem.ID && item.controllerIDRelated == null;
                                    }) ? 1 : 0;

                                    _.each($scope.attributes[index].attributeOptions[index2].controllers, function (controllerItem, index3) {

                                        $scope.attributes[index].attributeOptions[index2].controllers[index3].selected = _.any(selected, function (item) {
                                            return item.attrIDRelated == attribute.ID && item.optIDRelated == optionItem.ID && item.controllerIDRelated == controllerItem.ID;
                                        }) ? 1 : 0;

                                    });

                                    $scope.attributes[index].open = $scope.attributes[index].open || _.any($scope.attributes[index].attributeOptions[index2].controllers.concat($scope.attributes[index].attributeOptions), function (item) {
                                        return item.selected;
                                    }) ? 1 : 0;

                                    $scope.attributes[index].attributeOptions[index2].open = $scope.attributes[index].attributeOptions[index2].open || _.any($scope.attributes[index].attributeOptions[index2].controllers, function (item) {
                                        return item.selected;
                                    }) ? 1 : 0;
                                })
                            });

                            $scope.cancel = function () {
                                $modalInstance.dismiss('cancel');
                            };

                            $scope.save = function () {

                                var related = [];
                                _.each($scope.attributes, function (attribute) {
                                    var relatedCount = related.length;
                                    if (attribute.selected == 1) {
                                        related.push([attribute.ID, null, null, attribute.type]);
                                    }
                                    _.each(attribute.attributeOptions, function (option) {
                                        if (option.selected == 1) {
                                            related.push([attribute.ID, option.ID, null, attribute.type]);
                                        }
                                        _.each(option.controllers, function (controller) {
                                            if (controller.selected == 1) {
                                                related.push([attribute.ID, option.ID, controller.ID, attribute.type]);
                                            }
                                        });
                                    });
                                });

                                ConfigOptionService.saveRelatedIncreases(optID, controllerID, related).then(function (data) {
                                    $modalInstance.dismiss('cancel');
                                    Notification.success($filter('translate')('success'));
                                    scope.getRelatedIncreasesCount(controllerID);
                                }, function (data) {
                                    Notification.error($filter('translate')('error'));
                                });
                            };

                            $scope.nodeClick = function (node) {
                                if (!node.selected) {
                                    node.open = !node.open;
                                }
                            };

                            $scope.checkSubnodes = function (node, childrenCollection, nextCollection) {
                                if (node.selected) {
                                    node.open = false;
                                    for (var c in node[childrenCollection]) {
                                        if (node[childrenCollection][c].selected) {
                                            node[childrenCollection][c].selected = false;
                                        }
                                    }
                                }
                                if (nextCollection) {
                                    for (var c in node[childrenCollection]) {
                                        node[childrenCollection][c].open = false;
                                        for (var n in node[childrenCollection][c][nextCollection]) {
                                            if (node[childrenCollection][c][nextCollection][n].selected) {
                                                node[childrenCollection][c][nextCollection][n].selected = false;
                                            }
                                        }
                                    }
                                }
                            };
                        }
                    });
                }
            }
        }

    })
    .directive('buttonTemplateVariables', function ($modal, $filter, Notification, TemplateVariablesService, StaticContentService, $rootScope) {
        return {
            restrict: 'E',
            template: '<button class="btn btn-xs {{buttonStyle}}" ng-click="configureVariables()" tooltip="{{\'view_settings\' | translate}}"><i class="fa fa-desktop"></i></button>',
            replace: true,
            link: function (scope, elem, attrs) {
                scope.buttonStyle = 'blue-hoki';// btn-warning
                // ====================================================================================
                // ====================================================================================
                // ====================================================================================
                var categoryID = attrs['category'];
                var groupID = attrs['group'];
                var typeID = attrs['type'];

                function getRange() {
                    if (categoryID) {
                        return 'category'
                    } else if (groupID) {
                        return 'group'
                    } else if (typeID) {
                        return 'type'
                    }
                }

                function getRangeID() {
                    if (categoryID) {
                        return categoryID
                    } else if (groupID) {
                        return groupID
                    } else if (typeID) {
                        return typeID
                    }
                }


                TemplateVariablesService.getTemplates().then(function (templates) {
                    TemplateVariablesService.getGlobalVariables().then(function (globalVariables) {
                        TemplateVariablesService.getAll().then(function (templateVariables) {
                            TemplateVariablesService.getForRange(getRange(), getRangeID()).then(function (contextTemplateVariables) {
                                var templateNames = Object.fromEntries(templates.map(function (item) {
                                    return [item.ID, item.name]
                                }));
                                templates.filter(function (item) {
                                    if (getRange() === 'category') {
                                        return item.name === 'category'
                                    } else if (getRange() === 'group') {
                                        return item.name === 'group'
                                    } else if (getRange() === 'type') {
                                        return item.name === 'calc'
                                    }
                                }).forEach(function (template) {
                                    template.templateName = templateNames[template.ID];
                                    var variablesForTemplate = templateVariables.filter(function (variable) {
                                        return variable.templateName == template.name
                                    });
                                    template.variables = variablesForTemplate.map(function (variable) {
                                        var current = globalVariables.find(function (item) {
                                            return item.templateVariableTypeID == variable.ID;
                                        });
                                        var currentFoRange = contextTemplateVariables.find(function (item) {
                                            return item.templateVariableTypeID == variable.ID;
                                        });

                                        variable.valuesArray = variable.values.split('|').map(function (value) {
                                            return {
                                                name: value,
                                                selected: current ? current.value == value : false,
                                                selected2: currentFoRange != undefined && currentFoRange.value == value,
                                                ID: current ? current.ID : null,
                                                templateVariableTypeID: current ? current.templateVariableTypeID : null
                                            }
                                        });
                                        return variable;
                                    })
                                });

                                var isDifferent = false;
                                templates.forEach(function (template) {
                                    if (template.variables) {
                                        template.variables.forEach(function (variable) {
                                            if (variable.valuesArray) {
                                                variable.valuesArray.forEach(function (value) {
                                                    if (value.selected2 && value.selected === false) {
                                                        isDifferent = true;
                                                    }
                                                });
                                            }
                                        });
                                    }
                                });
                                if (isDifferent) {
                                    scope.buttonStyle = 'btn-warning';//
                                }
                            });
                        });
                    });
                });

                // ====================================================================================
                // ====================================================================================
                // ====================================================================================


                scope.configureVariables = function (e) {
                    var categoryID = attrs['category'];
                    var groupID = attrs['group'];
                    var typeID = attrs['type'];

                    function getRange() {
                        if (categoryID) {
                            return 'category'
                        } else if (groupID) {
                            return 'group'
                        } else if (typeID) {
                            return 'type'
                        }
                    }

                    function getRangeID() {
                        if (categoryID) {
                            return categoryID
                        } else if (groupID) {
                            return groupID
                        } else if (typeID) {
                            return typeID
                        }
                    }

                    $modal.open({
                        templateUrl: 'shared/templates/modalboxes/template-variables.html',
                        scope: scope,
                        resolve: {
                            templates: function () {
                                return TemplateVariablesService.getTemplates().then(function (data) {
                                    return data;
                                });
                            },
                            globalVariables: function () {
                                return TemplateVariablesService.getGlobalVariables().then(function (data) {
                                    return data;
                                });
                            },
                            templateVariables: function () {
                                return TemplateVariablesService.getAll().then(function (data) {
                                    return data;
                                });
                            },
                            contextTemplateVariables: function () {
                                return TemplateVariablesService.getForRange(getRange(), getRangeID()).then(function (data) {
                                    return data;
                                });
                            }
                        },
                        controller: function ($scope, $modalInstance, templates, globalVariables, templateVariables, contextTemplateVariables) {
                            $scope.templateStatic = {};

                            TemplateVariablesService.getAll().then(function (variables) {
                                variables.forEach(function (variable) {
                                    StaticContentService.getContent('variables.' + variable.name).then(function (data) {
                                        if (data.contents) {
                                            $scope.templateStatic[variable.name] = data.contents[$rootScope.currentLang.code];
                                        }
                                    });
                                });
                            });

                            function dataToView(templates, globalVariables, templateVariables, contextTemplateVariables) {
                                var templateNames = Object.fromEntries(templates.map(function (item) {
                                    return [item.ID, item.name]
                                }));
                                templates.filter(function (item) {
                                    if (getRange() === 'category') {
                                        return item.name === 'category'
                                    } else if (getRange() === 'group') {
                                        return item.name === 'group'
                                    } else if (getRange() === 'type') {
                                        return item.name === 'calc'
                                    }
                                }).forEach(function (template) {
                                    template.templateName = templateNames[template.ID];
                                    var variablesForTemplate = templateVariables.filter(function (variable) {
                                        return variable.templateName == template.name
                                    });
                                    template.variables = variablesForTemplate.map(function (variable) {
                                        var current = globalVariables.find(function (item) {
                                            return item.templateVariableTypeID == variable.ID;
                                        });
                                        var currentFoRange = contextTemplateVariables.find(function (item) {
                                            return item.templateVariableTypeID == variable.ID;
                                        });

                                        variable.valuesArray = variable.values.split('|').map(function (value) {
                                            return {
                                                name: value,
                                                selected: current ? current.value == value : false,
                                                selected2: currentFoRange != undefined && currentFoRange.value == value,
                                                ID: current ? current.ID : null,
                                                templateVariableTypeID: current ? current.templateVariableTypeID : null
                                            }
                                        });
                                        return variable;
                                    })
                                });
                                $scope.templateVariables = templates;
                            }

                            dataToView(templates, globalVariables, templateVariables, contextTemplateVariables);
                            $scope.cancel = function () {
                                $modalInstance.dismiss('cancel');
                            };

                            $scope.saveVariable = function (variable, value) {
                                var data = {};
                                data.ID = variable.ID;
                                data.value = value.name;
                                data.templateVariableTypeID = value.templateVariableTypeID;
                                data.categoryID = categoryID;
                                data.groupID = groupID;
                                data.typeID = typeID;
                                data.range = getRange();
                                TemplateVariablesService.updateAssoc(value.ID, data).then(function (data) {
                                    Notification.success($filter('translate')('success'));
                                    TemplateVariablesService.getForRange(getRange(), getRangeID()).then(function (data) {
                                        dataToView(templates, globalVariables, templateVariables, data);
                                    });
                                }, function (data) {
                                    Notification.error($filter('translate')('error'));
                                });
                            };

                        }
                    });
                }
            }
        }

    })
    .directive('simpleUploadInput', function () {
        return {
            restrict: 'A',
            link: function (scope, elem, attrs) {
                var s=elem[0].style
                s.opacity=s.width=s.height=0
                elem.parent()[0].className='btn btn-xs btn-success'
                elem.on('change', function(e){
                    scope.$eval(attrs.suichange,e)(e);
                });
                elem.on('$destroy', function() {
                    elem.off();
                });
            }
        }

    })
