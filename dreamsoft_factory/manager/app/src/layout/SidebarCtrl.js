angular.module('digitalprint.app')
  .controller('layout.SidebarCtrl', function($scope, $state, $window, $rootScope, DomainService, Notification){

      function readDomains(force){
          DomainService.getAll(force).then(function(data){
              $rootScope.domains = data;
          });
      }
      readDomains()
      $rootScope.$on('newDomainAdd',function(){
          readDomains(true)
      })

    $scope.changeDomain = function(domainId) {
      DomainService.setDomain(domainId).then(function(data) {
      	Notification.success('Domain changed');
      	$window.location.reload();
      });

      $('body').toggleClass('page-quick-sidebar-open'); 
    }

  });
