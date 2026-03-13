angular.module('digitalprint.app')
    .controller('superadmin.LangExportImportCtrl', function ($scope, $q, $filter, $config, $modal, $location,
                                                             UploadService, LangRootService, LangSettingsRootService,
                                                             LangService, LangSettingsService, Notification) {

        var isShopContext=$location.path().indexOf('/shop')>-1;

        var MyLangSettingsService=isShopContext?LangSettingsService:LangSettingsRootService;
        var MyLangService=isShopContext?LangService:LangRootService;

        MyLangSettingsService.getAll().then(function (data) {
            $scope.langlist = data;
        });

        $scope.createForm = function () {
            $scope.form = {};
        };

        $scope.uploader = UploadService.getUploader(MyLangService.getUploaderUrl('import'));

        $scope.createForm();

        $scope.exportLang = function () {
            MyLangService.export($scope.form.exportLang).then(function (data) {
                if (data.response) {
                    $modal.open({
                        templateUrl: 'shared/templates/modalboxes/files.html',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.filesTitle = 'translation_export';
                            $scope.files = [data.url];
                            $scope.fileLabel = 'filesLabel';
                        }
                    });
                } else {
                    Notification.error(Notification.error($filter('translate')('error')));
                }
            });
        };

        $scope.importLang = function () {
            UploadService.upload($scope.uploader, {
                'lang': $scope.form.importLang
            }).then(function (data) {
                if (data.response) {
                    Notification.success(Notification.success($filter('translate')('success')));
                    $scope.createForm();
                } else {
                    Notification.error(Notification.error($filter('translate')('error')));
                }
            });
        };
    });
