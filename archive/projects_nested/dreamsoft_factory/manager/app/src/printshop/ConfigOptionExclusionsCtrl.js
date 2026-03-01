angular.module('digitalprint.services')
    .controller('printshop.ConfigOptionExclusionsCtrl', function ($scope, $filter, $q, $rootScope, getData, Notification,
                                                                  PsConfigOptionService, PsConfigAttributeService) {
        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        $scope.attribute = getData.attribute;
        $scope.exclusionsChange = false;
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var ConfigOptionAllOptions = new PsConfigOptionService(0);
        var ConfigOptionService = new PsConfigOptionService(currentAttrID);

        $q.all([ConfigOptionAllOptions.getAll(), ConfigOptionService.getExclusions(currentOptID), PsConfigAttributeService.getAll(true)]).then(function(data){
            $scope.allOptions = _.groupBy(data[0], 'attrID');

            $scope.exclusions = _.isArray(data[1]) && data[1].length==0 ? {}:data[1];

            $scope.attributes = data[2];
            $scope.attrsToExclusions = _.filter($scope.attributes, function (attr) {
                return attr.ID != $scope.attribute.ID
            });
            updateCounted();
        });

        $scope.refresh = function () {
            $scope.exclusionsCancel();
        };
        function updateCounted() {
            $scope.allSelections = [];
            _.each($scope.attrsToExclusions, function (attr, i) {
                attr.selectedChildren = $scope.exclusions[attr.ID] ? _.map($scope.exclusions[attr.ID], function (j, excl) {
                    return _.find($scope.allOptions[attr.ID], function (opt) {
                        return opt.ID == excl;
                    }).name;
                }) : [];
                _.each(attr.selectedChildren, function (name) {
                    $scope.allSelections.push(attr.name + ' ' + name);
                });
            })
        }

        $scope.setExclusion = function (attrID, optID) {
            $scope.exclusionsChange = true;

            if ($scope.exclusions[attrID] === undefined) {
                $scope.exclusions[attrID] = {};
            }


            if ($scope.exclusions[attrID][optID] !== 1) {
                $scope.exclusions[attrID][optID] = 1;
            } else {
                $scope.exclusions[attrID] = _.omit($scope.exclusions[attrID], optID.toString());

                if (_.keys($scope.exclusions[attrID]).length === 0) {
                    delete $scope.exclusions[attrID];
                }
            }
            updateCounted();
        };

        $scope.exclusionsSave = function () {

            var exclusions = angular.copy($scope.exclusions);

            var excResult = [];

            for (var attributeID in exclusions) {
                for (var optionID in exclusions[attributeID]) {
                    if (exclusions[attributeID][optionID] == 1) {
                        excResult.push({'excAttrID': attributeID, 'excOptID': optionID});
                    }
                }
            }

            ConfigOptionService.saveExclusions(currentOptID, excResult).then(function () {
                $scope.exclusionsChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });


        };

        $scope.exclusionsCancel = function () {
            ConfigOptionService.getExclusions(currentOptID).then(function (data) {
                $scope.exclusions = data;
            }, function (data) {
                console.log(data);
            });
            $scope.exclusionsChange = false;
        };
        $scope.selectAllImpl = function (attrID,allSelectionState) {
            $scope.exclusionsChange = true;
            $scope.allOptions[attrID].forEach(function(options){
                if(!$scope.exclusions[attrID]){
                    $scope.exclusions[attrID]={};
                }
                $scope.exclusions[attrID][options.ID] = allSelectionState;
            });
        }
    });
