angular.module('digitalprint.services')
  .service('DpUserAddressService', function($q, $http, $config) {

    var DpUserAddressService = function(userID) {
      this.userID = userID;
      this.resource = ['users', this.userID, 'address'].join('/');
    }

    DpUserAddressService.prototype.getAllAddresses = function() {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'GET',
        url: $config.API_URL + _this.resource + '?type=1'
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    DpUserAddressService.prototype.getAllAddressesVat = function() {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'GET',
        url: $config.API_URL + _this.resource + '?type=2'
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    DpUserAddressService.prototype.createAddress = function(data) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'POST',
        url: $config.API_URL + _this.resource,
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    DpUserAddressService.prototype.edit = function(data) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'PUT',
        url: $config.API_URL + _this.resource,
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    DpUserAddressService.prototype.remove = function(data) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'DELETE',
        url: $config.API_URL + [_this.resource, data.ID].join('/'),
        data: data
      }).success(function(data) {
        if (data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    return DpUserAddressService;
  })