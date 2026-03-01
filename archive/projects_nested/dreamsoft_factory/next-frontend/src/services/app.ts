javascript
// Ensure we stay within the range
const clampValue = (newVal, min, max) => {
    if (newVal < min) {
        newVal = min;
    }
    if (newVal > max) {
        newval = max;
    }
    return newVal;
};

// 7) Additionally, you can observe changes in $scope,
// to live-fix the value.
// Here we use "vm.fixValueAndNotify()" in watch:
$scope.$watch(() => vm.model, () => {
    vm.fixValueAndNotify();
});

const rangeClamp = (min, max) => ({
    restrict: 'A',
    controllerAs: 'vm',
    controller: ['$scope', ($scope) => {
        $scope.$watch(() => vm.model, () => {
            vm.model = clampValue(vm.model, min, max);
            vm.fixValueAndNotify();
        });
    }]
});
