import axios from 'axios';
import { RefObject } from 'react';

interface Product {
  currentPages?: number;
  attrPages: any[];
  info: { noCalculate?: boolean };
}

interface NewProduct {
  pages: number;
  options: [];
  attrPages: any[];
}

interface Item {
  products: NewProduct[];
}

const processProduct = (product: Product, newItem: Item, scope: { complexProducts: Product[], length: number }, index: number): Promise<void> => {
    const def = { promise: new Promise((resolve) => {
        let newProduct: NewProduct = {};

        if (product.currentPages !== undefined) {
            newProduct.pages = product.currentPages;
        } else {
            newProduct.pages = 2;
        }
        newProduct.options = [];

        removeEmptyOptionFromSelected(product, newProduct);

        newProduct.attrPages = product.attrPages;

        if (product.info.noCalculate !== true) {
            newItem.products.push(newProduct);
        }

        if ((scope.complexProducts.length - 1) === index) {
            resolve(newItem);
        }
    })};

    return def.promise;
}

const removeEmptyOptionFromSelected = (product: Product, newProduct: NewProduct): void => {
    // implementation
}

const showSumPrice = ($scope: any) => {
    if ($scope.calculation !== undefined) {
        let price = parseFloat($scope.calculation.priceTotal);
    }
}