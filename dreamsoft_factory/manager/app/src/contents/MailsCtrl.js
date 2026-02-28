angular.module('digitalprint.app')
  .controller('contents.MailsCtrl', function($scope, MailTypeService, Notification){

    MailTypeService.getAll().then(function(data) {
      $scope.mailTypes = data;
    }, function(data) {
      Notification.error($filter('translate')('error'));
    });

  });