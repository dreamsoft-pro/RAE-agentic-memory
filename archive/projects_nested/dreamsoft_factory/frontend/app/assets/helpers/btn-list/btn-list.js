angular.module('dpClient.helpers')
    .directive('btnList', function () {
        return {
            restrict: 'E',
            scope: {items: '=', labelFn: '=', compareFn: '=', clickFn: '=ngClick', overallClasses:'=', model:'=ngModel'},
            replace: true,
            link: (scope, element, attrs) => {

            },
            template: `<div class="btn-list"><button
                            ng-repeat="item in items"
                            ng-class="{'list-group-item-info':compareFn(item, model)}"
                            ng-click="clickFn(item, model)"
                            class="{{overallClasses}} custom-list-view list-group-item class-custom-select-box">{{labelFn?labelFn(item):item.name}}</button></div>`
        }
    })
