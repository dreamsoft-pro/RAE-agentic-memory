angular.module('digitalprint.helpers')
    .directive('dpDatepicker', [
        function () {
            return {
                restrict: 'A',
                replace: true,
                require: 'ngModel',
                scope: {
                    myChange: '=ngChange',
                    model: '=ngModel',
                    ngRequired: '=',
                    modelName: '@ngModel'
                },
                template: function (elements, attrs) {
                    return '<p class="input-group input-group-sm">' +
                        '<input ng-change="changed()" ng-required="ngRequired" type="text" class="form-control" datepicker-popup="yyyy-MM-dd" ' +
                        'datepicker-append-to-body="false" ng-model="dateValue" is-open="opened" datepicker-options="{startingDay: 1}" ' +
                        'clear-text="{{ \'clear\' | translate }}" current-text="{{ \'today\' | translate }}" close-text="{{ \'close\' | translate }}" />' +
                        '<span class="input-group-btn">' +
                        '<button type="button" class="btn btn-default" ng-click="openDate($event)"><i class="glyphicon glyphicon-calendar"></i></button>' +
                        '</span>' +
                        '</p>';
                },
                link: function (scope, element, attrs) {

                },
                controller: function ($scope, $timeout, $filter, $modal, $sce, $attrs) {
                    $scope.opened = false;

                    $scope.$watch('model', function (newVal) {
                        if ($scope.model instanceof Date && !isNaN($scope.model.getTime())) {
                            var date = $scope.model;
                            $scope.dateValue = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
                            $scope.model = new Date(date).valueOf() / 1000;
                        }
                    });

                    $scope.$parent.$watch($scope.modelName, function(newVal) {
                        if( newVal === null ) {
                            $scope.dateValue = newVal;
                        }
                    });

                    $scope.changed = function () {

                        if( $scope.dateValue === undefined ) {
                            return;
                        }

                        if ($scope.dateValue !== null) {
                            $scope.model = $scope.dateValue.valueOf() / 1000;
                        }

                        if( $scope.dateValue === null) {
                            $scope.model = null;
                        }

                        if ($scope.myChange) {
                            $scope.myChange();
                        }
                    };

                    $scope.openDate = function ($event) {
                        $event.preventDefault();
                        $event.stopPropagation();
                        $scope.opened = !$scope.opened;
                    };

                }
            };
        }]);