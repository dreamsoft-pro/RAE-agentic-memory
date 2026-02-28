angular.module('digitalprint.services')
    .service('ProductFileService', function ($q, Restangular, $http, $config, Upload) {

        var ProductFileService = {};

        ProductFileService.getUrl = function (productID) {
            return $config.API_URL + ['dp_products', productID, 'productFiles'].join('/');
        };

        ProductFileService.getAll = function (productID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: this.getUrl(productID)
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ProductFileService.removeFile = function (productID, fileID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: this.getUrl(productID) + '/' + fileID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ProductFileService.acceptReport = function (productID, fileID) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: this.getUrl(productID) + '/' + fileID + '/productReportFiles'
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ProductFileService.uploadFile = function (file, productID, cpAttrID, fileID) {
            return Upload.upload({
                url: ProductFileService.getUrl(productID) + '/' + cpAttrID,
                fields: {update: true, fileID},
                file: file
            });
        };
        ProductFileService.addFile = function (file, productID, cpAttrID) {
            return Upload.upload({
                url: ProductFileService.getUrl(productID) + '/' + cpAttrID,
                file: file
            });
        };


        return ProductFileService;

    });
