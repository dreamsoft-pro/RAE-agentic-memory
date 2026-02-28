import { $q } from './httpBridge';
/**
 */

import React from "react";
import { useCalculator } from "../CalculatorContext";

export const Testing_and_Debugging = () => {
  const calc = useCalculator();


  // --- chunk_016.tsx ---



interface Product {
    excludedOptions: number[];
    selectedOptions: Record<string, number>;
}

interface Attribute {
    attrID: string;
    filteredOptions: { ID: number }[];
    attrName: string;
}

function handleProductExclusions(product: Product, attribute: Attribute) {
    const def = $q.defer();

    if (attribute && attribute.filteredOptions.length > 0) {
        _.each(attribute.filteredOptions, option => {
            if (!_.includes(product.excludedOptions, option.ID)) {
                product.excludedOptions.push(option.ID);
            }
        });

        product.selectedOptions[attribute.attrID] = attribute.filteredOptions[0].ID;

        CalcSimplifyWidgetService.removeUnActiveOptions(product).then(() => {
            setExclusionsAsync(product).then(() => {
                def.resolve(true);
            });
        });
    } else {
        console.log('Wykluczamy opcje dla atrybutu: ', attribute.attrName, product.selectedOptions[attribute.attrID]);
        delete product.selectedOptions[attribute.attrID];
        def.resolve(true);
    }

    return def.promise;
}

function addExcludesFromFormatAndPages(product: Product, exclusions: any[]) {
    const def = $q.defer();

    if (_.size(exclusions) > 0) {
        _.each(exclusions, exc => {
            _.each(exc, optID => {
                product.excludedOptions.push(optID);
            });
        });
        def.resolve(true);
    } else {
        def.resolve(true);
    }

    return def.promise;
}

function aggregateSelectedOptions(product: Product) {
    const def = $q.defer();

    const aggregateSelectedOptions: number[] = [];

    _.each(product.selectedOptions, selectedOptID => {
        aggregateSelectedOptions.push(selectedOptID);
    });

    def.resolve(aggregateSelectedOptions);

    return def.promise;
}
  // --- chunk_017.tsx ---





const ProductComponent = ({ productId }) => {
  const [product, setProduct] = useState({ selectedOptions: {}, excludedOptions: [] });
  const { loading, error, data } = useQuery(GET_PRODUCT_ATTRIBUTES, { variables: { id: productId } });

  useEffect(() => {
    if (data && data.product) {
      setProduct(data.product);
    }
  }, [data]);

  const addExcludedOptions = async (product, attribute) => {
    const aggregateSelectedOptions = await aggregateSelectedOptionsAsync(product);
    let deletedAttrs = [];
    const size = _.size(attribute.options);

    for (let option of attribute.options) {
      if (_.intersection(aggregateSelectedOptions, option.excludesOptions).length > 0) {
        if (!product.excludedOptions.includes(option.ID)) {
          product.excludedOptions.push(option.ID);
        }
      }
    }
  };

  const aggregateSelectedOptionsAsync = async (product) => {
    // Implementation for aggregating selected options
    return [];
  };

  const checkAttrSelectAsync = async (product) => {
    let firstFilteredOption = null;

    for (let attribute of product.attributes) {
      if (deletedAttrs.includes(attribute.attrID)) {
        if (product.selectedOptions[attribute.attrID]) {
          firstFilteredOption = _.first(attribute.filteredOptions);
          if (firstFilteredOption) {
            product.selectedOptions[attribute.attrID] = firstFilteredOption.ID;
          }
        } else {
          attribute.filteredOptions = attribute.options.filter((opt) => !product.excludedOptions.includes(opt.ID));
          firstFilteredOption = _.first(attribute.filteredOptions);
          if (firstFilteredOption) {
            const flat = _.reduceRight(firstFilteredOption.exclusions, (a, b) => a.concat(b), []);
            product.excludedOptions = { ...product.excludedOptions, ...flat };
            product.selectedOptions[attribute.attrID] = firstFilteredOption.ID;
          }
        }
      }
    }
  };

  const checkRelatedFormats = (format) => {
    if (!format.relatedFormats) {
      return true;
    }
    // Implementation for checking related formats
  };

  return (
    <div>
      {/* Render your product details here */}
    </div>
  );
};

export default ProductComponent;
};
