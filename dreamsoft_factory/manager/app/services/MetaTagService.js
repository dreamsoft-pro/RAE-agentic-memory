angular.module('digitalprint.services')
    .service('MetaTagService', function($rootScope, $q, $http, $config, Restangular){

        var MetaTagService = {};

        var resource = 'dp_mainMetaTags';


        MetaTagService.getUploadUrl = function (resource) {
            if (resource === undefined){
                resource='dp_mainMetaTags';
            }
            return $config.API_URL + [resource, 'uploadImage'].join('/');
        };

        MetaTagService.get = function (ID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, ID].join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MetaTagService.add = function(metaTag, routeID) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource].join("/"),
                data: {
                    'languages': metaTag.languages,
                    'routeID': routeID
                }
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MetaTagService.edit = function(metaTag,images, resource) {
            if (resource === undefined){
                resource='dp_mainMetaTags';
            }
            var def = $q.defer();
            console.log(metaTag);
            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, metaTag.ID].join("/"),
                data: {
                    'languages': metaTag.languages,
                    'routeID': metaTag.routeID,
                    'ID': metaTag.ID
                }
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MetaTagService.deleteImage = function (lang, imageID, resource) {
            console.log('coś tam jednak działa');
            if (resource === undefined){
                resource='dp_mainMetaTags';
            }
            var def = $q.defer();


            var uploadResource = [resource];
            uploadResource.push('uploadImage');
            var rs = uploadResource.join('/');
            console.log('remove url',rs);
            Restangular.all(rs).one(lang,imageID).remove().then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return MetaTagService;
    });