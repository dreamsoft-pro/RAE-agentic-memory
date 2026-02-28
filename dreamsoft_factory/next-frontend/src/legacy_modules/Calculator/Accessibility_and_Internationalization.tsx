import { $q } from './httpBridge';
/**
 */

import React from "react";
import { useCalculator } from "../CalculatorContext";

export const Accessibility_and_Internationalization = () => {
  const calc = useCalculator();


  // --- chunk_014.tsx ---





interface Product {
    excludedOptions?: any;
    excludedByAttribute?: {};
    attributes?: Array<{
        filteredOptions: any;
    }>;
    attributeMap?: Array<string>;
    selectedOptions?: {};
}

const setExclusionsAsync = (product: Product) => {
    const def = $q.defer();

    product.excludedOptions = _.clone(product.formatExcluded);
    product.excludedByAttribute = {};

    _.each(product.attributes, (attribute) => {
        attribute.filteredOptions = _.clone(attribute.options, true);
    });

    let optID: any;
    let activeAttrID: string | undefined;
    _.each(product.attributeMap, (attrID) => {
        activeAttrID = attrID;
        optID = product.selectedOptions[attrID];

        if (optID) {
            const item = _.isObject(optID) ? optID : getOption(product, optID);
            if (!item) {
                def.reject('no item for optID ' + optID);
                return def.promise;
            }
            let tmpExclusions: any = {};

            const printExcl = (all: any, label: string) => {
                _.each(all, (item, i) => {
                    if (item.length) console.log('excluded ' + label, item);
                });
            };

            const exclusionsThickness = calc.filterByThickness(product);
            printExcl(exclusionsThickness, 'exclusionsThickness');
            const exclusionsThicknessPages = calc.filterByOptionsPages(product);
            printExcl(exclusionsThicknessPages, 'exclusionsThicknessPages');

            if (item.exclusions) {
                tmpExclusions = _.merge({}, item.exclusions, exclusionsThickness, exclusionsThicknessPages);
            }

            product.excludedByAttribute[activeAttrID] = _.merge({}, item.exclusions);

            setOptionExclusionsAsync(product, activeAttrID, tmpExclusions).then((isEnd) => {
                if (isEnd) {
                    checkAttrSelectAsync(product).then((isAttrSelectEnd) => {
                        if (isAttrSelectEnd) {
                            if (_.last(product.attributeMap) === activeAttrID) {
                                const attrIndex = _.findIndex(product.attributes, { 'attrID': attrID });
                                if (attrIndex > -1) {
                                    if (product.attributes[attrIndex].filteredOptions.length !== $('#select-attribute-' + attrID + " option").length) {
                                        product.attributes[attrIndex] = { ...product.attributes[attrIndex], filteredOptions: [] }; // Update the filteredOptions property
                                    }
                                }
                            }
                            def.resolve();
                        } else {
                            def.reject('isAttrSelectEnd failed');
                        }
                    });
                } else {
                    def.reject('setOptionExclusionsAsync failed');
                }
            }).catch((error) => {
                def.reject(error);
            });
        });
    });

    return def.promise;
};
  // --- chunk_015.tsx ---

 // Assuming next-api is a mock for $q in Next.js

interface Product {
    attributes: Attribute[];
    attributeMap: number[];
    excludedOptions: string[];
    selectedOptions: { [key: string]: string };
}

interface Attribute {
    attrID: number;
    filteredOptions: Option[];
    options: Option[];
}

interface Option {
    ID: string;
    exclusions?: string[][];
}

async function setOptionExclusionsAsync(product: Product, attrID: number, exclusions: string[]) {
    const def = $q.defer();

    let attribute = _.find(product.attributes, { attrID });

    await addExcludesFromFormatAndPages(product, exclusions);
    await addExcludedOptions(product, attribute);

    attribute.filteredOptions = _.filter(attribute.options, (opt) => !_.includes(product.excludedOptions, opt.ID));

    let selectedOption = _.find(attribute.filteredOptions, { ID: product.selectedOptions[attrID] });

    if (!selectedOption) {
        if (attribute.filteredOptions.length > 0) {
            const oldSelectedOptionID = product.selectedOptions[attrID];
            const oldOptionIndex = _.findIndex(attribute.options, { ID: oldSelectedOptionID });

            if (oldOptionIndex > -1) {
                const flatExclusions = _.flatMap(_.reverse([...attribute.options[oldOptionIndex].exclusions]));
                product.excludedOptions = product.excludedOptions.filter((item) => !flatExclusions.includes(item));
            }

            const flatNewExclusions = _.flatMap(_.reverse([...attribute.filteredOptions[0].exclusions]));
        }
    }
}

};
