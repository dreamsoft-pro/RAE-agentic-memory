javascript
import { BackendApi } from '@/lib/api';

ProductFileService.saveFileProps = (productID, fileID, data) => {
    return new Promise((resolve, reject) => {
        const url = `${BackendApi.API_URL}/dp_products/${productID}/productFiles/saveFileProps/${fileID}`;
        BackendApi.post(url, data)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

ProductFileService.saveProductProps = (productID, sendToFix) => {
    return new Promise((resolve, reject) => {
        const url = `${BackendApi.API_URL}/dp_products/${productID}/productFiles/saveProductProps`;
        BackendApi.post(url, { sendToFix })
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};
