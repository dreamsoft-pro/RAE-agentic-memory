angular.module('digitalprint.app')
    .controller('shop.LangsCtrl', function ($scope, $filter, $modal, LangService, Notification) {


        $scope.langs = [];
        $scope.pagination = {
            perPage: 25,
            currentPage: 1
        };

        $scope.pagination.setPage = function (pageNo) {
            $scope.pagination.currentPage = pageNo;
        };

        LangService.getAll().then(function (data) {
            $scope.langs = data;
            $scope.filterLangs = _.clone($scope.langs);

        });

        $scope.edit = function (lang) {
            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-lang.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(lang);
                    $scope.lang = lang;

                    $scope.ok = function () {
                        LangService.edit($scope.form).then(function (data) {
                            if (!!data.localID) {
                                $scope.form.localID = data.localID;
                            }
                            $scope.form.change = true;
                            var idx = _.findIndex($scope.langs, {ID: lang.ID});
                            $scope.langs[idx] = _.clone($scope.form);
                            $scope.search(false);
                            //TODO
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }
                }
            });
        };

        $scope.search = function (setFirstPage) {
            if (_.isUndefined(setFirstPage)) {
                setFirstPage = true;
            }
            console.log($scope.filterData);
            $scope.filterLangs = $filter('filter')(
                $scope.langs,
                $scope.filterData
            );
            if (setFirstPage) {
                $scope.pagination.setPage(1);
            }
        };

        $scope.remove = function (elem) {

            var idx = _.findIndex($scope.langs, {
                ID: elem.ID
            });

            LangService.remove(elem.localID + '').then(function () {
                $scope.langs[idx].change = false;
                delete $scope.langs[idx].value;
                $scope.search(false);
                Notification.success($filter('translate')('success'));
            });

        }

    });