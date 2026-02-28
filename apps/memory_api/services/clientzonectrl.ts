javascript
const menuTop = [];
_.each(topMenuList, (element) => {
    if(element !== null) {
        menuTop.push(element);
    }
});
$scope.menuTop = menuTop;

const menuBottom = [];
var bottomMenuList = [
    $state.get('client-zone-data'),
    $state.get('client-zone-delivery-data'),
    $state.get('client-zone-invoice-data'),
    $state.get('client-zone-change-pass')
];
_.each(bottomMenuList, (element) => {
    if(element !== null) {
        menuBottom.push(element);
    }
});
$scope.menuBottom = menuBottom;

$scope.usedSpace = 0;
if($rootScope.companyID === 195 || $rootScope.companyID === 35) {
    $scope.usedSpace = (parseInt($rootScope.user.userID) * 1234) % 1000;
    $scope.showQuota = true;
}

// [BACKEND_ADVICE] The logic for calculating usedSpace and showQuota should be moved to the backend service if it involves complex business rules or large datasets.

$scope.search = function() {
    // Search functionality implementation goes here
};
