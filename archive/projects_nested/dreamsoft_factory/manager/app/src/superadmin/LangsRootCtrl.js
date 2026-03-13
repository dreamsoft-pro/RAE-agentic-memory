angular.module('digitalprint.app')
    .controller('superadmin.LangsRootCtrl', function ($scope, $rootScope, $filter, $modal, LangRootService,
                                                      LangSettingsRootService, Notification) {

        $scope.langlist = [];
        $scope.form = {};

        LangSettingsRootService.getAll().then(function (data) {
            $scope.langlist = data;
            $scope.form.lang = _.first($scope.langlist).code;
        });

        $rootScope.$on('LangSettingsRoot.getAll', function (e, data) {
            $scope.langlist = data;
            $scope.form.lang = _.first($scope.langlist).code;
        });

        $scope.langs = [];
        $scope.pagination = {
            perPage: 25,
            currentPage: 1
        };

        $scope.pagination.setPage = function (pageNo) {
            $scope.pagination.currentPage = pageNo;
        };

        LangRootService.getAll().then(function (data) {
            $scope.langs = data;
            $scope.filterLangs = _.clone($scope.langs);

        });

        $scope.add = function () {
            LangRootService.create($scope.form).then(function (data) {
                $scope.langs.push(data);
                $scope.form = {};
                $scope.form.lang = _.first($scope.langlist).code;
                $scope.search(false);
                Notification.success("Ok");
            })
        };

        $scope.edit = function (lang) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/edit-lang.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(lang);

                    $scope.ok = function () {
                        LangRootService.update($scope.form).then(function (data) {
                            lang = _.extend(lang, $scope.form);
                            $modalInstance.close();
                            Notification.success("Ok");
                        });
                    }
                }
            });
        };

        $scope.search = function (setFirstPage) {
            if (_.isUndefined(setFirstPage)) {
                setFirstPage = true;
            }

            _.each($scope.filterData, function (item, idx) {
                if (item === null) {
                    $scope.filterData[idx] = '';
                }
            });

            $scope.filterLangs = $filter('filter')(
                $scope.langs,
                $scope.filterData
            );
            if (setFirstPage) {
                $scope.pagination.setPage(1);
            }
        };

        $scope.remove = function (id) {

            var idx = _.findIndex($scope.langs, {
                ID: id
            });

            LangRootService.remove(id).then(function () {
                $scope.langs.splice(idx, 1);
                $scope.search(false);
                Notification.success('Success');
            });

        }


    });