angular.module('digitalprint.directives')
    .run(['$templateCache',
        function ($templateCache) {
            $templateCache.put("template/faqAccordion/buttonFaqAccordion.html",
                '<button ng-click="open()" class="btn btn-primary btn-sm">\n' +
                '<i class="fa fa-info-circle"></i> <span ng-if="buttonName">{{ buttonName }}</span>' +
                '<span ng-if="!buttonName">{{ "help" | translate }}</span>' +
                '</button>'
            );
        }
    ])
    .directive('buttonFaqAccordion', function ($modal, AdminHelpService) {

        return {
            restrict: 'A',
            templateUrl: 'template/faqAccordion/buttonFaqAccordion.html',
            replace: true,
            scope: {
                buttonName: '@buttonName'
            },
            link: function (scope, elem, attrs) {

                scope.open = function () {
                    $modal.open({
                        size: 'lg',
                        template: '<div class="modal-header">' +
                        '<h3 class="modal-title"><span ng-if="buttonName">{{ buttonName }}</span><span ng-if="!buttonName">{{ "help" | translate }}</span></h3>' +
                        '</div>' +
                        '<div class="modal-body" ><div><div faq-accordion="' + attrs.buttonFaqAccordion + '"></div></div><div class="modal-footer"><button class="btn red-sunglo" ng-click="$dismiss()">{{ "close" | translate }}</button></div></div>'

                    });
                }
            }
        }

    });