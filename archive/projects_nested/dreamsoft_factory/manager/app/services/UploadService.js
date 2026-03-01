'use strict';

angular.module('digitalprint.services')
    .factory('UploadService', function ($q, $http, $config, Restangular, FileUploader) {

        var UploadService = {};

        var resourceGraphics = getGraphicsResource();
        var resourceTA = getTextAngularUploadResource();

        function getGraphicsResource() {
            return 'graphicsUpload';
        }

        function getTextAngularUploadResource() {
            return 'taUploadIcons';
        }

        UploadService.getLogoUploadUrl = function () {
            return $config.API_URL + [resourceGraphics].join('/');
        };

        UploadService.getTAUploadUrl = function () {
            return $config.API_URL + [resourceTA].join('/');
        };
        UploadService.getModelIconsUploadUrl = function () {
            return $config.API_URL + [resourceGraphics, 'modelIcon'].join('/');
        };

        UploadService.getFaviconUploadUrl = function () {
            return $config.API_URL + [resourceGraphics, 'favicon'].join('/');
        };

        UploadService.getModelFiles = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resourceGraphics, 'modelIcon'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        UploadService.getUploader = function (url) {
            return new FileUploader({
                url: url,
                autoUpload: false,
                queueLimit: 1,
                removeAfterUpload: true
            });
        };

        UploadService.upload = function (uploader, formData) {
            var def = $q.defer();
            uploader.onSuccessItem = function (item, data) {
                def.resolve(data);
            };
            var file = uploader.queue[0];
            uploader.data = {};
            file.formData = [formData];
            uploader.uploadItem(file);
            return def.promise;
        };

        return UploadService;

    });
