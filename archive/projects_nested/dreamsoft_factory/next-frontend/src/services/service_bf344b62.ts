import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

class ProductFileService {
    static getUrl(productID: string | number): string {
        return `${API_URL}/dp_products/${productID}/productFiles`;
    }

    static getUploadUrl(productID: string | number, attrID: string | number): string {
        return `${API_URL}/dp_products/${productID}/productFiles/${attrID}`;
    }

    static fixFileDimensions(productID: string | number, fileID: string | number) {
        const url = this.getUploadUrl(productID, fileID);
        return axios.put(url).then(response => response.data).catch(error => Promise.reject(error));
    }
}

export default ProductFileService;