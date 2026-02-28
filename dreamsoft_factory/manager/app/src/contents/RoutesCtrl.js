'use strict';
angular.module('digitalprint.app')
  .controller('contents.RoutesCtrl', function($scope, $filter, $cacheFactory, ConfigService,
                                              TemplateRootService, RouteService, Notification, $modal) {


    $scope.sortChange = false;

    $scope.sortableOptions = {
      stop: function(e, ui) {
        $scope.sortChange = true;
      },
      axis: 'y',
      placeholder: 'success',
      handle: 'fa.icon-cursor-move',
      cancel: ''
    };

    function init() {
      $scope.routes = [];
      $scope.refresh(true);
    }

    $scope.refresh = function(fromCache) {
      var force = true;

      if (!!fromCache) {
        force = false
      }

      RouteService.getAll(force).then(function(data) {
        $scope.routes = data;
        doSmthWithMyData(data);
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });

      TemplateRootService.getAll().then(function(data) {
        $scope.templates = data;
      })
    };

    function doSmthWithMyData(data) {
      var collection = _.clone(data, true);
      $scope.routesList = [];
      _.each(collection, function(item) {
        getItem(item, $scope.routesList, 0);
      });

    }

    function getItem(item, collection, level) {
      if(!!level) {
        for(var i = 0; i < level; i++) {
          //console.log('level', i)
          item.state = '-----' + item.state;
        }
      }
      //console.log('item', item, level);
      collection.push(item);
      if(item.children) {
        level++;
        _.each(item.children, function(child) {
          getItem(child, collection, level);

        });
      }

    }

    $scope.template = function(route) {
      $modal.open({
        templateUrl: 'src/contents/templates/modalboxes/route-template.html',
        scope: $scope,
        resolve: {
          routeTemplates: function() {
            return TemplateRootService.getTemplates(route.ID).then(function(data) {
              //console.log(data)
              return data;
            }, function(data) {
              Notification.error($filter('translate')('data'))
            });
          },
          templates: function() {
            return TemplateRootService.getAll().then(function(data) {
              return data;
            }, function(data) {
              Notification.error($filter('translate')('error'))
            });
          }
        },
        controller: function($scope, $modalInstance, routeTemplates, templates) {

          $scope.route = _.clone(route, true);
          $scope.routeTemplates = _.clone(routeTemplates, true)
          $scope.templates = _.clone(templates, true)

          $scope.remove = function(template) {
            TemplateRootService.removeTemplateFromRoute(template.ID, route.ID).then(function(data) {
              var idx = _.findIndex($scope.templates, {ID: template.ID});
              if(idx > -1) {
                $scope.routeTemplates.splice(idx, 1);
              }
            });
          };

          $scope.ok = function() {
            $scope.form.routeID = route.ID;

            TemplateRootService.setTemplate($scope.form).then(function(data) {
              //console.log(data);
              $scope.routeTemplates.push(data.item);
              Notification.success($filter('translate')('success'));
            }, function(data) {
              Notification.error($filter('translate')('error') + ' ' + data.info);
            })
          }
        }
      })
    };

    $scope.add = function() {
      RouteService.create($scope.form).then(function(data) {
        //console.log($scope.form);
        $scope.refresh();
        $scope.form = {};
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    };

    $scope.editStart = function(route) {
      $modal.open({
        templateUrl: 'src/contents/templates/modalboxes/edit-route.html',
        scope: $scope,
        controller: function($scope, $modalInstance) {
          $scope.form = _.clone(route, true);
          
          $scope.save = function() {
            RouteService.edit($scope.form).then(function(data) {
              $scope.refresh();
              $modalInstance.close();
              Notification.success($filter('translate')('success'));
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });

          };

          $scope.cancel = function() {
            $modalInstance.close();
          }

        }

      })
    };

      $scope.removeGroup = function (elem) {
          RouteService.remove(elem.state).then(function (data) {
              $scope.refresh();
              Notification.success($filter('translate')('removed') + " " + elem.name);
          }, function (data) {
              Notification.error($filter('translate')('error'));
          });
      };

      $scope.resetDomain = function () {

          if ( confirm($filter('translate')('reset_own_settings'))) {
              ConfigService.resetDomain().then( function(data) {
                  if( data.response === true ) {
                      Notification.success("Zresetowano ustawienia");
                      $scope.refresh(false);
                  } else {
                      Notification.error("Error");
                  }
              });
          } else {
              console.log('2');

          }
      };

      init();


  });