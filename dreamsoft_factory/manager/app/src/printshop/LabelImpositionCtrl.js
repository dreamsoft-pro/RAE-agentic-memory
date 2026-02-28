angular.module('digitalprint.app')
    .controller('printshop.LabelImpositionCtrl', function ($scope, $stateParams, $filter, Notification, LabelImpositionService) {
        const currentTypeID = $stateParams.typeID;


        function fixTypes() {
            $scope.labelImposition.labelRotation = $scope.labelImposition.labelRotation+''
            $scope.labelImposition.rotationAngle = $scope.labelImposition.rotationAngle+''
        }

        LabelImpositionService.getForType(currentTypeID).then(function(data) {
            if (data) {
                $scope.labelImposition = data;
                if (!$scope.labelImposition.ID) {
                    $scope.labelImposition.labelRotation = 0
                    $scope.labelImposition.rotationAngle = 0
                }
                fixTypes()
            }
        })

        $scope.update = function(data) {
            LabelImpositionService.update(data).then(function(result) {
                if (result) {
                    $scope.labelImposition = result
                    fixTypes()
                    Notification.success($filter('translate')('saved'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            })
        }
    }).controller('LabelImpositionVariablesCtrl', function ($scope){
    $scope.isCollapsed = false
    $scope.variables = ['order_number']
}).controller('LabelImpositionVariables2Ctrl', function ($scope){
    $scope.isCollapsed = false
    $scope.variables = ['order_number', 'user_name', 'user_email', 'user_last_name','die_cut_file_name']
})
