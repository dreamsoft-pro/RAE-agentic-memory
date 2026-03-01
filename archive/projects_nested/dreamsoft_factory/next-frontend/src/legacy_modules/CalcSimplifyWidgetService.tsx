import { $q } from './httpBridge';
/**
 * Service: CalcSimplifyWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import _ from 'lodash';
import { $q } from 'angular'; // Assuming $q is a part of angular, replace with appropriate import if different

angular.module('digitalprint.services')
    .factory('CalcSimplifyWidgetService', function ($q) {
        const checkFormatExclusions = (product: any, format: any) => {
            const def = $q.defer();

            if (!product.currentFormat) {
                def.reject('no product.currentFormat');
                return def.promise;
            }
            product.formatExcluded = [];

            _.each(product.attributes, (attribute, attributeIndex) => {
                if (!attribute.options && (product.attributes.length - 1) === attributeIndex) {
                    def.resolve(true);
                }

                _.each(attribute.options, (option, optionIndex) => {
                    if (option && option.formats) {
                        if (!_.includes(option.formats, product.currentFormat.ID)) {
                            product.formatExcluded.push(option.ID);
                            if (product.selectedOptions[attribute.attrID] === option.ID) {
                                delete product.selectedOptions[attribute.attrID];
                            }
                        }
                    }

                    if ((product.attributes.length - 1) === attributeIndex && (attribute.options.length - 1) === optionIndex) {
                        def.resolve(true);
                    }
                });
            });

            return def.promise;
        };

        const removeUnActiveOptions = (product: any) => {
            const def = $q.defer();

            let index = 0;
            _.each(product.attributeMap, (attrID) => {
                const attributeIndex = _.findIndex(product.attributes, { attrID });

                if (product.selectedOptions[attrID] === undefined) {
                    if ((product.attributeMap.length - 1) > index) {
                        def.resolve(true);
                    }
                } else {
                    if (attributeIndex > -1 && product.attributes[attributeIndex].filteredOptions.length === 0) {
                        delete product.selectedOptions[attrID];
                    }
                    if ((product.attributeMap.length - 1) > index) {
                        def.resolve(true);
                    }
                }

                index++;
            });

            return def.promise;
        };

        const markEmptyOptions = (product: any) => {
            const emptyOptions = [];
            _.each(product.selectedOptions, (optID, attrID) => {
                const idx = _.findIndex(product.attributes, { attrID: parseInt(attrID) });
                if (idx > -1 && product.attributes[idx].filteredOptions.length === 0) {
                    emptyOptions.push(optID);
                }
            });

            return emptyOptions;
        };

        const removeEmptyOptionFromSelected = (product: any, newProduct: any) => {
            const def = $q.defer();
            const emptyOptions = markEmptyOptions(product);

            _.each(product.selectedOptions, (optID, attrID) => {
                if (!optID || !_.includes(emptyOptions, optID)) {
                    newProduct.options.push({
                        attrID: parseInt(attrID),
                        optID: optID
                    });
                }
            });

            def.resolve(newProduct);
            return def.promise;
        };

        const prepareProductPromise = (scope: any, newItem: any) => {
            const def = $q.defer();

            newItem.products = [];
            _.each(scope.complexProducts, (complexProduct, index) => {
                const product = complexProduct.selectedProduct.data;

                const newProduct = {};

                newProduct.groupID = product.info.groupID;
                newProduct.typeID = product.info.typeID;
                newProduct.name = product.info.typeName;

                if (!product.currentFormat) {
                    console.error('Formats must be assign!');
                }

                newProduct.formatID = product.currentFormat.ID;

                if (!product.currentFormat.custom) {
                    // Calculation for width and height based on format type
                    if (product.currentFormat.type === 'standard') {
                        newProduct.width = product.currentFormat.width;
                        newProduct.height = product.currentFormat.height;
                    } else {
                        newProduct.width = product.currentFormat.customWidth + product.currentFormat.slope * 2;
                        newProduct.height = product.currentFormat.customHeight + product.currentFormat.slope * 2;
                    }
                }

                if (product.currentPages) {
                    newProduct.pages = product.currentPages;
                } else {
                    newProduct.pages = 2;
                }

                removeEmptyOptionFromSelected(product, newProduct);

                newProduct.attrPages = product.attrPages;

                if (product.info.noCalculate !== true) {
                    newItem.products.push(newProduct);
                }
            });

            def.resolve(newItem);
            return def.promise;
        };

        const showSumPrice = () => {
            // Implementation for showing sum price
        };

        const showSumGrossPrice = () => {
            // Implementation for showing sum gross price
        };

        return {
            checkFormatExclusions,
            removeUnActiveOptions,
            prepareProductPromise,
            showSumPrice,
            showSumGrossPrice
        };
    });