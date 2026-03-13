angular.module('dpClient.helpers')
    /**
     * Display element if translation exists
     * @example
     * <div lang-conditional="'lang_key_name'" class="my-class">
     *         </div>
     * @example
     * <div lang-conditional="'lang_key_name'">
     *     <div>content...</div>
     *         </div>
     */
    .directive('langConditional', function ($compile, $filter) {
        return {
            restrict: 'A',
            link: (scope, element, attrs) => {
                const translation = $filter('translate')(attrs['langConditional']);
                if (!translation || translation == attrs['langConditional']) {
                    element.replaceWith('')
                } else if (element[0].childNodes.length == 1 && element[0].childNodes[0].nodeType == 3) {
                    element.text(translation)
                }
            }
        };
    })
