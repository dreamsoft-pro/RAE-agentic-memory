javascript
import { cancelTimeout, setTimer } from '@/lib/api';

$scope.setParams = function () {
    cancelTimeout(updateTableTimeout);
    updateTableTimeout = setTimer(() => {
        $scope.customProductsCtrl.get();
    }, 600);
};

// [BACKEND_ADVICE] Handle date filtering logic
$scope.filterOffersDate = function() {
    if ($scope.offerFilters.dateFrom && $scope.offerFilters.dateTo) {
        $scope.customProductsCtrl.params.dateFrom = Math.floor($scope.offerFilters.dateFrom.getTime() / 1000);
        $scope.customProductsCtrl.params.dateTo = Math.floor(($scope.offerFilters.dateTo.getTime() + (60 * 60 * 24)) / 1000);
        $scope.setParams();
    }
};

$scope.clearFilters = function(){
    $scope.customProductsCtrl.params.dateFrom = null;
    $scope.customProductsCtrl.params.dateTo = null;
    $scope.offerFilters = {
        dateFrom: null,
        dateTo: null
    };
    $scope.setParams();
};
