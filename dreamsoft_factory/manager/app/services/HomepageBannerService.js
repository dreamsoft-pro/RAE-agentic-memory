'use strict';

angular.module('digitalprint.services')
.factory('HomepageBannerService', function($q, $http, $config, Restangular) {
	var HomePageBannerService ={};

	function getResource() {
		return 'homePageBanner';
	}
	var resource = getResource();

	HomePageBannerService.getAll = function() {
		var def = $q.defer();	

		$http({
			method: 'GET',
			url: $config.API_URL + resource
		}).success(function(data) {
			def.resolve(data);
		}).error(function(data) {
			def.reject(data);
		});

		return def.promise;
	}	
	HomePageBannerService.add = function(files) {
		var def = $q.defer();	

		$http({
			method: 'POST',
			url: $config.API_URL + resource,
			data: files
		}).success(function(data) {
			def.resolve(data);
		}).error(function(data) {
			def.reject(data);
		});

		return def.promise;
	}
	HomePageBannerService.addLink = function(link) {
		var def = $q.defer();	
		
		$http({
			method: 'POST',
			url: $config.API_URL + resource,
			data: link
		}).success(function(data) {
			def.resolve(data);
		}).error(function(data) {
			def.reject(data);
		});

		return def.promise;
	}
	return HomePageBannerService;
});