'use strict';

var tinymce = window.tinymce;

angular.module('dreamsoft.tinymce', [])

  .value('dsTinymceConfig', {})

  .directive('dsTinymce', ['$rootScope', '$compile', '$timeout', '$window', '$sce', 'dsTinymceConfig', 'dsTinymceService', function($rootScope, $compile, $timeout, $window, $sce, dsTinymceConfig, dsTinymceService) {

    dsTinymceConfig = dsTinymceConfig || {};

    if (dsTinymceConfig.baseUrl) {
      tinymce.baseURL = dsTinymceConfig.baseUrl;
    }

    return {
      require: ['ngModel', '^?form'],
      priority: 599,
      link: function(scope, element, attrs, ctrls) {
        if (!$window.tinymce) {
          return;
        }

        var ngModel = ctrls[0],
          form = ctrls[1] || null;

        var expression, options = {
          debounce: true,
          toolbar: 'bold italic underline strikethrough nonbreaking | searchreplace preview fullscreen insertdatetime | emoticons alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | cut copy paste | undo redo | link unlink image media | table hr removeformat | subscript superscript blockquote code | forecolor backcolor fontselect fontsizeselect formatselect styleselect | visualblocks visualchars charmap preview fullscreen insertdatetime searchreplace spellchecker template pagebreak anchor emoticons help | table tabledelete | tableprops tablerowprops tablecellprops | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol',
          plugins: 'lists link image table visualchars searchreplace preview nonbreaking advlist insertdatetime fullscreen emoticons'
        }, tinyInstance,
          updateView = function(editor) {
            var content = editor.getContent({format: options.format}).trim();
            content = $sce.trustAsHtml(content);
            ngModel.$setViewValue(content);
            if (!$rootScope.$phase) {
              scope.$digest();
            }
          };

        function toggleDisable(disabled) {
          if (disabled) {
            ensureInstance();
            if (tinyInstance) {

              tinyInstance.getBody().setAttribute('contenteditable', false);

            }
          } else {
            ensureInstance();

            if (tinyInstance && tinyInstance.getBody().getAttribute('contenteditable') === false && tinyInstance.getDoc()) {

              tinyInstance.getBody().setAttribute('contenteditable', true);

            }
          }
        }

        var uniqueId = dsTinymceService.getUniqueId();
        attrs.$set('id', uniqueId);

        expression = {};
        angular.extend(expression, scope.$eval(attrs.dsTinymce));

        var debouncedUpdate = (function(debouncedUpdateDelay) {
          var debouncedUpdateTimer;
          return function(ed) {
            $timeout.cancel(debouncedUpdateTimer);
            debouncedUpdateTimer = $timeout(function() {
              if (ed.isDirty()) {
                ed.save();
                updateView(ed);
              }
            }, debouncedUpdateDelay);
          };
        })(400);

        var setupOptions = {
          setup: function(ed) {
            ed.on('init', function() {
              ngModel.$render();
              ngModel.$setPristine();
              ngModel.$setUntouched();
              if (form) {
                form.$setPristine();
              }
            });

            ed.on('ExecCommand change NodeChange ObjectResized', function() {
              if (!options.debounce) {
                ed.save();
                updateView(ed);
                return;
              }
              debouncedUpdate(ed);
            });

            ed.on('blur', function() {
              element[0].blur();
              ngModel.$setTouched();
              if (!$rootScope.$phase) {
                scope.$digest();
              }
            });

            ed.on('remove', function() {
              element.remove();
            });

            if (dsTinymceConfig.setup) {
              dsTinymceConfig.setup(ed, {
                updateView: updateView
              });
            }

            if (expression.setup) {
              expression.setup(ed, {
                updateView: updateView
              });
            }
          },
          format: expression.format || 'html',
          target: element[0]
        };

        angular.extend(options, dsTinymceConfig, expression, setupOptions);

        $timeout(function() {
          if (options.baseURL) {
            tinymce.baseURL = options.baseURL;
          }
          tinymce.init(options).then(function(editors) {
            tinyInstance = editors[0];
            toggleDisable(scope.$eval(attrs.ngDisabled));
          });
        });

        ngModel.$formatters.unshift(function(modelValue) {
          return modelValue ? $sce.trustAsHtml(modelValue) : '';
        });

        ngModel.$parsers.unshift(function(viewValue) {
          return viewValue ? $sce.getTrustedHtml(viewValue) : '';
        });

        ngModel.$render = function() {
          ensureInstance();
          var viewValue = ngModel.$viewValue ? $sce.getTrustedHtml(ngModel.$viewValue) : '';
          if (tinyInstance) {
            tinyInstance.setContent(viewValue);
            tinyInstance.fire('change');
          }
        };

        attrs.$observe('disabled', toggleDisable);

        scope.$on('$destroy', function() {
          ensureInstance();
          if (tinyInstance) {
            tinyInstance.remove();
            tinyInstance = null;
          }
        });

        function ensureInstance() {
          if (!tinyInstance) {
            tinyInstance = tinymce.get(attrs.id);
          }
        }
      }
    };
  }])

  .service('dsTinymceService', [function() {
    var DSTinymceService = function() {
      var ID_ATTR = 'ds-tinymce';
      var uniqueId = 0;
      var getUniqueId = function() {
        uniqueId++;
        return ID_ATTR + '-' + uniqueId;
      };
      return {
        getUniqueId: getUniqueId
      };
    };
    return new DSTinymceService();
  }]);
