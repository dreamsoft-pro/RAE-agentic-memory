	'use strict';

angular.module('digitalprint.services')
	.factory('TypeDescriptionsFormatsService', function($q, $http, $config, Restangular) {

	var TypeDescriptionsFormatsService = {};
			var resource = getResource();

		function getResource() {
			return 'ps_typeDescriptionsFormats';

		}
		TypeDescriptionsFormatsService.getAll = function(descID) {
			var def = $q.defer();	

			$http({
				method: 'GET',
				url: $config.API_URL + resource + '?dID='+descID
			}).success(function(data) {
				def.resolve(data);
			}).error(function(data) {
				def.reject(data);
			});

			return def.promise;
	}
		TypeDescriptionsFormatsService.setFormats = function(descID, formats){
		var def = $q.defer();
		var postData = {};
		postData.descID = descID;
		postData.formats = formats;

			$http({
				method: 'POST',
				url: $config.API_URL + resource,
				data: postData
			}).success(function(data) {
				def.resolve(data);
			}).error(function(data) {
				def.reject(data);
			});

			return def.promise;
		}
		return TypeDescriptionsFormatsService;

	});