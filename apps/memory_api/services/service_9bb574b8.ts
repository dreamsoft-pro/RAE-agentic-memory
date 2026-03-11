import React from 'react';
import axios from '@/lib/api'; // Assuming this is correctly set up as Axios or similar

interface Attribute {
  attrID: number;
  options?: { ID: number }[];
}

interface Product {
  attributes?: Attribute[];
}

class FilterOptions extends React.Component<{ product: Product }> {
  filterByOptionsPages = async (product: Product): Promise<any> => {
    const exclusions: Record<number, number[]> = {};

    if (!product.attributes) return exclusions;

    for (const attribute of product.attributes) {
      exclusions[attribute.attrID] = [];

      if (!attribute.options) continue;

      for (const option of attribute.options) {
        const idx = attribute.options.findIndex(opt => opt.ID === option.ID);
        
        if (idx === -1) {
          exclusions[attribute.attrID].push(option.ID);
        }
      }
    }

    return exclusions;
  };

  componentDidMount() {
    // Example usage, replace with actual logic
    this.filterByOptionsPages(this.props.product).then(exclusions => console.log(exclusions));
  }

  render() {
    return <div>Filter Options Component</div>;
  }
}

export default FilterOptions;