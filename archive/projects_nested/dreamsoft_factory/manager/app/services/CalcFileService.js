angular.module('digitalprint.services')
    .service('CalcFileService', function ($q, $http, $config) {

        var CalcFileService = {};

        var resource = ['dp_products', 'calcFilesUploader'].join('/');

        CalcFileService.getUrl = function (typeID) {
            return $config.API_URL + ['dp_products', typeID, 'calcFilesUploader'].join('/');
        };


        CalcFileService.getAllByType = function (typeID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: this.getUrl(typeID)
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CalcFileService.removeFile = function (typeID, fileID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: this.getUrl(typeID) + '/' + fileID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };




        CalcFileService.getAll = function (setID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + ['dp_products', setID, 'calcFilesUploaderSet'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        return CalcFileService;

    });
