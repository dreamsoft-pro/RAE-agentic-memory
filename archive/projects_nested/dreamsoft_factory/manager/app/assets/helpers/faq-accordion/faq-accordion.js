angular.module('digitalprint.directives')
  .run(['$templateCache',
    function ($templateCache) {
      $templateCache.put("template/faqAccordion/faqAccordion.html",
        "<div class=\"panel-group \" id='{{module}}'>\n" +
        "  <div  ng-repeat=\"item in accordions\" class=\"panel panel-{{ item.addClass || 'default' }}\">\n" +
        "    <div class=\"panel-heading\" data-target=\"#{{ item.ID + $index }}\" data-toggle=\"collapse\" data-parent=\"#{{module}}\">\n" +
        "      <h4 class=\"panel-title\">\n" +
        "      <a class=\"accordion-toggle\">{{ item.texts[currentLang.code].title }}</a>\n" +
        "      </h4>\n" +
        "    </div>\n" +
        "    <div id=\"{{ item.ID + $index }}\" class=\"panel-collapse collapse\" style=\"\">\n" +
        "      <div class=\"panel-body\" ng-bind-html=\"item.texts[currentLang.code].description\">\n" +
        "      </div>\n" +
        "    </div>\n" +
        "  </div>\n" +
        "  <div ng-if='!accordions.length'>Empty module: {{module}}</div>\n" +
        "</div>"
        );
    }
  ])
  .directive('faqAccordion', function (AdminHelpService) {

    return {
      restrict: 'A',
      templateUrl: 'template/faqAccordion/faqAccordion.html',
      replace: true,
      link: function(scope, elem, attrs){
        scope.prefix = _.uniqueId('accordion_');
        scope.module = attrs.faqAccordion;

        AdminHelpService.getModule(attrs.faqAccordion).then(function(data) {
          scope.accordions = _.map(data, function(item){
            item.ID = scope.prefix + item.ID;
            return item;
          });
        })

      }
    }

  });