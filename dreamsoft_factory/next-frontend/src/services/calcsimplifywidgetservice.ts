javascript
import { backendApi } from '@/lib/api';
import _ from 'lodash';

const CalcSimplifyWidgetService = {
    checkFormatExclusions: function(product, format) {
        const def = Promise.defer();

        if (!product.currentFormat) {
            return def.reject('no product.currentFormat');
        }
        product.formatExcluded = [];

        _.each(product.attributes, (attribute, attributeIndex) => {
            if (!attribute.options && (product.attributes.length - 1) === attributeIndex) {
                return def.resolve(true);
            }

            _.each(attribute.options, (option, optionIndex) => {

                // [BACKEND_ADVICE] Heavy logic should be moved to backend API calls
                backendApi.checkFormatExclusion(product.id, format.id)
                    .then(response => {
                        product.formatExcluded.push(response.exclusionReason);
                        if (attributeIndex === product.attributes.length - 1 && optionIndex === attribute.options.length - 1) {
                            def.resolve(true);
                        }
                    })
                    .catch(error => {
                        def.reject(error.message);
                    });
            });
        });

        return def.promise;
    }
};

export default CalcSimplifyWidgetService;
