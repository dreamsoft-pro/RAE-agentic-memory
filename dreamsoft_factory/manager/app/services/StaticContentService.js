/**
 * Created by Rafał on 19-06-2017.
 */
'use strict';

angular.module('digitalprint.services')
    .factory('StaticContentService', function($q, $http, $config) {

        var StaticContentService = {};
        var resource = getResource();

        function getResource() {
            return ['dp_static_contents'];
        }

        StaticContentService.getAll = function() {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        StaticContentService.create = function(data) {

            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        StaticContentService.update = function(data) {

            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        StaticContentService.remove = function(id){
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        StaticContentService.getContent = function(key) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getContent', key].join('/')
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        return StaticContentService;

    });