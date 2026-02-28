javascript
'use strict';

const { BackendService } = require('@/lib/api');

/**
 * @description
 * Controller for handling upload functionalities.
 */
class UploadCtrl {
  constructor($scope) {
    this.$scope = $scope;
    this.init();
  }

  init() {
    this.$scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  }
}

UploadCtrl.$inject = ['$scope'];

module.exports = UploadCtrl;
