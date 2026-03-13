/**
 * Created by Rafał on 19-06-2017.
 */
'use strict';
angular.module('digitalprint.app')
    .controller('contents.StaticContentsCtrl', function ($scope, $filter, $cacheFactory, $modal,
                                                         StaticContentService, $document, Notification) {

        $scope.contents = [];
        $scope.form = {};

        function init() {
            $(".bootstrap-switch").bootstrapSwitch();

            $(".bootstrap-switch").on('switchChange.bootstrapSwitch', function(event, state) {
                $scope.toggleSwitch(state);
            });

            $scope.resetForm();

            StaticContentService.getAll().then( function (data) {
                $scope.contents = data;
            });
        }

        $scope.resetForm = function() {
            $scope.form = {
                forDomain: 0,
                contents: {},
                key: ''
            };
        };

        $scope.add = function() {

            if( _.isEmpty($scope.form.contents) ) {
                Notification.warning($filter('translate')('select_all_required_fields'));
            }
            StaticContentService.create($scope.form).then(function (data) {
                if( data.response === true ) {
                    Notification.success($filter('translate')('success'));
                    $scope.resetForm();
                    $scope.contents.push(data.one);
                }
            });

        };

        $scope.toggleSwitch = function( state ) {
            $scope.form.forDomain = state ? 1 : 0;
        };

        $scope.edit = function( content ) {
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/edit-static-content.html',
                scope: $scope,
                keyboard: false,
                controller: function ($scope, $modalInstance) {

                    $scope.initModal = function() {
                        $(".bootstrap-switch-forDomain").bootstrapSwitch('state', content.forDomain ? true : false);

                        $(".bootstrap-switch-forDomain").on('switchChange.bootstrapSwitch', function(event, state) {
                            $scope.toggleSwitch('forDomain', state);
                        });

                        $(".bootstrap-switch-active").bootstrapSwitch('state', content.active ? true : false);

                        $(".bootstrap-switch-active").on('switchChange.bootstrapSwitch', function(event, state) {
                            $scope.toggleSwitch('active', state);
                        });
                    };

                    $scope.form = content;

                    $scope.save = function () {

                        StaticContentService.update($scope.form).then(function (data) {
                            if( data.response === true ) {
                                Notification.success($filter('translate')('success'));
                                var idx = _.findIndex($scope.contents, {ID: $scope.form.ID});
                                if( idx  > -1 ) {
                                    $scope.contents[idx] = data.one;
                                }
                                $modalInstance.close();
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        });
                    };

                    $scope.cancel = function() {
                        $modalInstance.close();
                    };

                    $scope.toggleSwitch = function( name, state ) {
                        $scope.form[name] = state ? 1 : 0;
                    };
                }
            });
        };

        $scope.remove = function(content) {
            StaticContentService.remove(content.ID).then( function(data) {
                if( data.response === true ) {
                    Notification.success($filter('translate')('success'));
                    var idx = _.findIndex($scope.contents, {ID: content.ID});
                    if( idx  > -1 ) {
                        $scope.contents.splice(idx, 1);
                    }
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });
        };

        init();

    });