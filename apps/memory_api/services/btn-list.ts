javascript
import { BackendAdvice } from '@/lib/api';

angular.module('dpClient.helpers')
    .directive('btnList', function () {
        return {
            restrict: 'E',
            scope: {
                items: '=',
                labelFn: '=',
                compareFn: '=',
                clickFn: '=ngClick',
                overallClasses: '=',
                model: '=ngModel'
            },
            replace: true,
            template: `<div class="btn-list">
                            <button
                                ng-repeat="item in items"
                                ng-class="{'list-group-item-info': compareFn(item, model)}"
                                ng-click="clickFn(item, model)"
                                class="{{ overallClasses }} custom-list-view list-group-item class-custom-select-box">
                                    {{ labelFn ? labelFn(item) : item.name }}
                            </button>
                        </div>`
        };
    });

// [BACKEND_ADVICE] Heavy logic should be moved to backend services for better maintainability and performance.
