import { $q } from './httpBridge';
/**
 */

import React from "react";
import { useCalculator } from "../CalculatorContext";

export const Integration_and_External_Services = () => {
  const calc = useCalculator();


  // --- chunk_010.tsx ---
Here's the modernized version of your code in Next.js with TypeScript:




interface Product {
    info: any;
    attributes: Array<{ attrID: string, options: Array<{ ID: string, default?: number }> }>;
    selectedOptions: Record<string, string>;
    excludedOptions: Array<string>;
}

const getCurrentCalcProduct = (product: Product['info']): any => {
    let currentCalcProduct = null;
    if (calc.currentCalc) {
        currentCalcProduct = _.find(calc.currentCalc.calcProducts, { typeID: product.typeID });
    }
    return currentCalcProduct;
};

calc.getProduct = async (product: Product) => {
    const def = $q.defer();

    let emptyProducts = 0;

    const newProduct: Partial<Product> = {
        info: product,
        selectedOptions: {},
        attrPages: {},
        attributes: {},
        attributeMap: [],
        optionMap: {},
        currentFormat: false,
        currentPages: false,
        excludedOptions: [],
        excludedByAttribute: {},
        formatExcluded: [],
        thickness: {
            values: {},
            min: null,
            max: null,
            current: null
        }
    };

    product.data = newProduct;

    const AttributeService = new PsAttributeService(product.groupID, product.typeID);
    const FormatService = new PsFormatService(product.groupID, product.typeID);
    const PagesService = new PsPageService(product.groupID, product.typeID);

    await $q.all([
        FormatService.getPublic(calc.complexID),
        PagesService.getPublic(),
        AttributeService.ge
    ]);
};

  // --- chunk_011.tsx ---
Here's the modernized version of your code in Next.js with TypeScript:





const ProductComponent = ({ product }) => {
    const [newProduct, setNewProduct] = useState({ formats: [], pages: [], attributes: [], attributeMap: [], optionMap: {} });
    const [emptyProducts, setEmptyProducts] = useState(0);
    const [countGroups, setCountGroups] = useState(0);
    const [currentCalcProduct, setCurrentCalcProduct] = useState(null);

    useEffect(() => {
        axios.get('/api/productData').then(({ data }) => {
            const formats = data[0];
            const attributesData = data[2];
            let emptyProducts = 0;

            if (attributesData.length === 0) {
                emptyProducts++;
            }

            if (emptyProducts === countGroups) {
                setEmptyProduct(true);
            }

            const customFormatIndex = _.findIndex(attributesData, { attrID: -1 });
            if (customFormatIndex > -1) {
                newProduct.customFormatInfo = attributesData[customFormatIndex];
                attributesData.splice(1, customFormatIndex);
            }

            const customPageIndex = _.findIndex(attributesData, { attrID: -2 });
            if (customPageIndex > -1) {
                newProduct.customPageInfo = attributesData[customPageIndex];
                attributesData.splice(1, customPageIndex);
            }

            newProduct.attributes = attributesData;

            _.each(newProduct.attributes, (attr) => {
                newProduct.attributeMap.push(attr.attrID);
                newProduct.optionMap[attr.attrID] = [];
                _.each(attr.options, (opt) => {
                    newProduct.optionMap[attr.attrID].push(opt.ID);
                });
            });

            newProduct.pages = data[1];

            newProduct.relatedFormats = _.clone(newProduct.formats);

            const formatIdx = currentCalcProduct ? _.findIndex(newProduct.relatedFormats, { ID: currentCalcProduct.formatID }) : -1;
            if (formatIdx === -1) {
                console.error('Can\'t find format like in select calculation.');
                return true;
            }

            const fetchFormat = async () => {
                await calc.selectFormatSync(newProduct, newProduct.relatedFormats[formatIdx]);
                if (currentCalcProduct) {
                    await calc.selectPagesSync(newProduct, currentCalcProduct.pages);
                } else {
                    if (newProduct.pages.length && newProduct.pages[0].pages) {
                        await calc.selectPagesSync(newProduct, newProduct.pages[0].pages);
                    }
                    if (newProduct.pages.length && newProduct.pages[0].minPages) {
                        await calc.selectPagesSync(newProduct, newProduct.pages[0].minPages);
                    }
                }
            };

            fetchFormat().then(() => def.resolve(data));
        });
    }, [product, countGroups]);

    return <div>Product Component</div>;
};

This code assumes the use of React functional components with hooks (`useState` and `useEffect`), and it uses Axios for HTTP requests. The structure is adapted to a modern JavaScript environment using ES6+ features, including arrow functions, template literals, and object spread/rest operators where applicable.
};
