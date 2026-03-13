/**
 * Service: AttributeDetailsCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import _ from 'lodash';
import { AttributeFiltersService } from './services/AttributeFiltersService';
import { Notification } from './Notification'; // Assuming you have a Notification component or service

const AttributeDetailsCtrl: React.FC = () => {
    const [option, setOption] = useState({});
    const [products, setProducts] = useState<any[]>([]);
    const dispatch = useDispatch();
    const params = useParams();

    useEffect(() => {
        console.log(params);
        setOption({});
        setProducts([]);

        // Fetch products using options
        AttributeFiltersService.getProductsUsingOptions(sendData.attrID).then((allProducts) => {
            if (allProducts.length > 0) {
                const filteredProducts = _.filter(allProducts, (product) => {
                    return product.options.some((opt: any) => opt === data[0].ID);
                });
                setProducts(filteredProducts);
            }
        }).catch((error) => {
            console.error("Error fetching products:", error);
        });
    }, [params]);

    const createFilterPart = (items: any[], name: string, type: string, filterConfig: any, label?: string, hidden?: boolean, precision?: number): any[] => {
        let item = { name, type, title: !!label ? label : name, hidden };
        switch (type) {
            case 'multi-select':
            case 'multi-select-color':
                item.values = filterConfig[name].values;
                item.selectedValues = {};
                break;
            case 'range':
                item.minValue = filterConfig[name].minValue;
                item.maxValue = filterConfig[name].maxValue;
                let diff = filterConfig[name].maxValue - filterConfig[name].minValue;
                let step = 1;
                if (diff < 1) {
                    step = 0.01;
                } else if (diff < 10) {
                    step = 0.1;
                } else if (diff < 100) {
                    step = 1;
                } else {
                    step = Math.round(diff / 50);
                }
                item.options = {
                    floor: filterConfig[name].minValue,
                    ceil: filterConfig[name].maxValue,
                    step,
                    precision,
                    onChange: () => {
                        onInputChange();
                    },
                };
                break;
        }
        items.push(item);
        return items;
    };

    // get alt papers
    useEffect(() => {
        const dataSend = { attrID: 2, optID: data[0].ID };
        setAlternativePapers([]);
        AttributeFiltersService.getRelativePapers(dataSend).then((altPapersFilter) => {
            if (altPapersFilter.length > 0) {
                AttributeFiltersService.getAttributeFilters(dataSend.attrID).then((filterConfigData) => {
                    const filterConfig = filterConfigData.filterConfig;
                    let filterPartsAltPapers: any[] = [];
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'name', 'text', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'category', 'select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'group', 'select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'paper_type', 'select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'weight', 'range', filterConfig, null, false, 0);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'whiteness', 'range', filterConfig, null, false, 0);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'thickness', 'range', filterConfig, null, false, 3);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'opacity', 'range', filterConfig, null, false, 0);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'roughness', 'range', filterConfig, null, false, 0);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'certificates', 'multi-select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'printingTechniques', 'multi-select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'application', 'multi-select', filterConfig);
                    filterPartsAltPapers = createFilterPart(filterPartsAltPapers, 'color_hex', 'multi-select-color', filterConfig, 'paper_color');
                    altPapersFilter.forEach((fd: any) => {
                        const part = _.find(filterPartsAltPapers, { name: fd.name });
                        if (fd.valueType === 'min') {
                            part.minValue = fd.value;
                        } else if (fd.valueType === 'max') {
                            part.maxValue = fd.value;
                        } else if (part.type === 'multi-select' || part.type === 'multi-select-color') {
                            if (!part.selectedValues) {
                                part.selectedValues = [];
                            }
                            part.selectedValues[fd.value] = true;
                        } else if (fd.valueType === 'exact') {
                            part.value = String(fd.value);
                        }
                    });
                    AttributeFiltersService.search(2, filterPartsAltPapers).then((altPapers) => {
                        setAlternativePapers(altPapers);
                    });
                });
            }
        });
    }, [data]); // Assuming data is defined somewhere in the component or global state

    const downloadPDF = () => {
        console.log('started rendering');
        const downloadData = { optID: params.optid, altPapers: alternativePapers };
        AttributeFiltersService.downloadPDF(downloadData).then((downloadResponse) => {
            if (downloadResponse.success) {
                window.open(downloadResponse.link, '_blank');
            } else {
                Notification.error('unexpected_error'); // Assuming you have a translate function or method to handle translations
            }
        }).catch((error) => {
            console.error("Error downloading PDF:", error);
        });
    };

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default AttributeDetailsCtrl;