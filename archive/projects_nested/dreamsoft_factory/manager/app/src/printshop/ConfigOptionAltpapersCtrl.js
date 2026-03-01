angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionAltpapersCtrl', function ($rootScope, $scope, $modal, $stateParams, $filter, $state, $q, PsConfigAttributeService, PsConfigOptionService, SettingService, Notification, getData) {


        $scope.option = angular.copy(getData.option);
        $scope.form = getData.option;
        $scope.attr = getData.attribute;
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var currentOptID = parseInt($stateParams.optID);
        var currentAttrID = parseInt($stateParams.attrID);
        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        $scope.currentPaper = {};
        
        function loadData() {
            $q.all([PsConfigAttributeService.getAll(true), ConfigOptionService.getAll(true)]).then(function (data) {
                $scope.attributes = data[0];
                if (!$scope.showAll) {
                    $scope.attr = _.findWhere($scope.attributes, {ID: currentAttrID});
                    $rootScope.currentAttrName = $scope.attr.name;
                }
                $scope.options = data[1];
                _.each($scope.options, function (option) {
                    var attr = _.find($scope.attributes, function (attr) {
                        return option.attrID == attr.ID;
                    });
                    if (attr) {
                        option.attrName = attr.name;
                        option.sortAttr = attr.sort;
                    }
                });
                $scope.options = _.sortBy($scope.options, 'sortAttr');
            });
        }
        
        loadData();

       

        
        ConfigOptionService.getOne(currentOptID).then(function (data) {
            $scope.currentPaper = data;
            var settings = new SettingService('additionalSettings');
            $scope.filteredAttribute;
            settings.getAll().then(function (data) {
                $scope.filteredAttribute = data.filteredAttribute.value;

                $q.all([PsConfigAttributeService.getFilterConfig($scope.filteredAttribute),
                    ConfigOptionService.getRelativeOptionsFilter(currentOptID),
                    PsConfigAttributeService.getOptions($scope.filteredAttribute)
                ]).then(function (data) {                    
                    var filterConfigData = data[0];
                    var filterData = data[1];
                    var allOptions = data[2];
                    _.each(allOptions, function (item) {
                        item.descriptions.weight = item.weight
                        item.descriptions.thickness = item.pageSize
                        _.each(['certificates', 'printingTechniques', 'color_hex', 'application', 'category', 'group', 'paper_type'],
                            function (name) {
                                if(item.descriptions[name]){
                                    return;
                                }
                                item.descriptions[name] = item.descriptions[name] ? _.map(item.descriptions[name].split(','),
                                    function (value) {
                                        return value.trim()
                                    }):[]
                            })
                    });
        
        
                            var filterParts = [];
                            var filterConfig = filterConfigData.filterConfig;
                            var descriptionsMap = filterConfigData.descriptionsMap;
        
                            function createFilterPart(items, name, type, filterConfig, label, hidden, precision) {
                                try {
                                    items = _.clone(items);
                                    var item = {name: name, type: type, title: !!label ? label : name, hidden: hidden};
                                    switch (type) {
                                        case 'select':
                                        case 'multi-select':
                                        case 'multi-select-color':
                                            item.values = filterConfig[name].values;
                                            item.selectedValues = {};
                                            break;
                                        case 'range':
                                            item.minValue0 = item.minValue = filterConfig[name].minValue;
                                            item.maxValue0 = item.maxValue = filterConfig[name].maxValue;
                                            var diff = filterConfig[name].maxValue - filterConfig[name].minValue
                                            var step = 1
                                            if (diff < 1) {
                                                step = 0.01;
                                            } else if (diff < 10) {
                                                step = 0.1;
                                            } else if (diff < 100) {
                                                step = 1
                                            } else {
                                                step = Math.round(diff / 50);
                                            }
                                            item.options = {
                                                floor: filterConfig[name].minValue,
                                                ceil: filterConfig[name].maxValue,
                                                step: step,
                                                precision: precision,
                                                onChange: function () {
                                                    $scope.onInputChange.apply(this)
                                                }
                                            }
                                            break;
                                    }
                                    items.push(item);
                                } catch (e) {
                                    console.error('Problem while creating filter part '+ e.message);
                                }
                                return items;
                            }

                            var filterParts = createFilterPart(filterParts, 'name', 'text', filterConfig, 'name_of_atrritute');
                            filterParts = createFilterPart(filterParts, 'category', 'select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'group', 'select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'paper_type', 'select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'weight', 'range', filterConfig, null, false, 0);
                            filterParts = createFilterPart(filterParts, 'whiteness', 'range', filterConfig, null, false, 0);
                            filterParts = createFilterPart(filterParts, 'thickness', 'range', filterConfig, null, false, 3);
                            filterParts = createFilterPart(filterParts, 'opacity', 'range', filterConfig, null, false, 0);
                            filterParts = createFilterPart(filterParts, 'roughness', 'range', filterConfig, null, false, 0);
                            filterParts = createFilterPart(filterParts, 'certificates', 'multi-select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'printingTechniques', 'multi-select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'application', 'multi-select', filterConfig);
                            filterParts = createFilterPart(filterParts, 'color_hex', 'multi-select-color', filterConfig, 'paper_color');
                            _.each(filterData, function (fd) {
                                var part = _.findWhere(filterParts, {name: fd.name});
                                if (fd.valueType == 'min') {
                                    part.minValue = fd.value;
                                } else if (fd.valueType == 'max') {
                                    part.maxValue = fd.value;
                                } else if (part.type == 'multi-select' || part.type == 'multi-select-color') {
                                    if (!part.selectedValues) {
                                        part.selectedValues = [];
                                    }
                                    part.selectedValues[fd.value] = true;
                                }  else if (fd.valueType == 'exact') {
                                    part.value = String(fd.value);
                                }
                            });
                            $scope.filterParts = _.cloneDeep(filterParts);
        
                            $scope.withUnit = function (value, unit) {
                                if (!value) {
                                    return '-';
                                }
                                return value + ' ' + unit
                            }
        
                            var timerId;
        
                            $scope.onInputChange = function (force) {
                               
                                var categoryFilter = $scope.filterParts.find(function(element){
                                    return element.name === 'category';
                                });
                                var groupFilter = $scope.filterParts.find(function(element){
                                    return element.name === 'group';
                                });
                                var paperTypeFilter = $scope.filterParts.find(function(element){
                                    return element.name === 'paper_type';
                                });
                                
                                if(categoryFilter.value && categoryFilter.value !== ''){
                                    var newGroupValues = Object.keys(filterConfig.categoriesTree[categoryFilter.value]);
                                    groupFilter.values = newGroupValues;

                                    var newPaperTypeValues = [];
                                    _.each(newGroupValues, function (unit) {
                                        var tmpValues = Object.keys(filterConfig.categoriesTree[categoryFilter.value][unit]);
                                        newPaperTypeValues = newPaperTypeValues.concat(tmpValues);
                                    });
                                    paperTypeFilter.values = newPaperTypeValues;
                                }

                                if(groupFilter.value && groupFilter.value !== ''){
                                    if(categoryFilter.value && categoryFilter.value !== ''){
                                        var newPaperTypeValues = Object.keys(filterConfig.categoriesTree[categoryFilter.value][groupFilter.value]);
                                        paperTypeFilter.values = newPaperTypeValues;
                                    }else{
                                        var categoryKeys = Object.keys(filterConfig.categoriesTree);
                                        _.each(categoryKeys, function (unit) {
                                            if(groupFilter.value in filterConfig.categoriesTree[unit]){
                                                var newPaperTypeValues = Object.keys(filterConfig.categoriesTree[unit][groupFilter.value]);
                                                paperTypeFilter.values = newPaperTypeValues;
                                                categoryFilter.value = unit;
                                            }
                                        });  
                                    }
                                }

                                clearTimeout(timerId)
                                if (!(force === true)) {
                                    timerId = setTimeout(function () {
                                        $scope.onInputChange(true)
                                    }, 1000);
                                    return
                                }
                                $scope.filtersUsed = true;
                                ConfigOptionService.search($stateParams.attrID, $scope.filterParts).then(function (data) {
                                    $scope.filteredOptions = data
                                }, function (error) {
                                });
                            }

                            $scope.resetFilters = function () {
                                _.each($scope.filterParts, function (unit) {
                                    unit.selectedValues = {};
                                    unit.value = null;
                                    if (unit.type == 'range') {
                                        var part = _.findWhere(filterParts, { name: unit.name });
                                        unit.minValue = part.minValue;
                                        unit.maxValue = part.maxValue;
                                    }
                                });

                                var groupFilter = $scope.filterParts.find(function(element){
                                    return element.name === 'group';
                                });
                                var paperTypeFilter = $scope.filterParts.find(function(element){
                                    return element.name === 'paper_type';
                                });

                                groupFilter.values = filterConfig.group.values;
                                paperTypeFilter.values = filterConfig.paper_type.values;

                                $scope.onInputChange(true);
                            }
        
                            $scope.onColorClick = function (unit, value) {
                                if (value) {
                                    unit.selectedValues[value] = !unit.selectedValues[value];
                                } else {
                                    unit.selectedValues = {};
                                }
        
                                $scope.onInputChange();
                            }
        
                            $scope.save = function () {
                                var filter = [];
                                _.each($scope.filterParts, function (unit) {
                                    var description = _.findWhere(descriptionsMap, {name: unit.name})
                                    var item = {typeID: description ? description.ID : null, name: unit.name}
                                    if (unit.value) {
                                        item.value = unit.value;
                                        item.valueType = 'exact';
                                        filter.push(_.clone(item));
                                    }
                                    if (unit.minValue) {
                                        item.value = unit.minValue;
                                        item.valueType = 'min';
                                        filter.push(_.clone(item));
                                    }
                                    if (unit.maxValue) {
                                        item.value = unit.maxValue;
                                        item.valueType = 'max';
                                        filter.push(_.clone(item));
                                    }
                                    if (unit.selectedValues) {
                                        _.each(unit.selectedValues, function (value, key) {
                                            if (value) {
                                                item.value = key;
                                                item.valueType = 'exact';
                                                filter.push(_.clone(item));
                                            }
                                        });
                                    }
                                });
                                console.log('filter');
                                console.log(filter);
                                ConfigOptionService.saveRelativeOptionsFilter(currentOptID, filter).then(function (data) {
                                    Notification.success($filter('translate')('success'));
                                    loadData();
                                }, function (data) {
                                    Notification.error($filter('translate')('error'));
                                });
                            };
        
                            $scope.cancel = function () {
                            
                            }
                            $scope.onInputChange();
                    
                });
            });
        });
    });
