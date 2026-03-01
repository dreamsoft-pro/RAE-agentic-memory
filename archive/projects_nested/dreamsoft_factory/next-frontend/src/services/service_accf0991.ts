import axios from 'axios';
import { API_URL } from '@/config'; // Adjust the import based on your actual configuration setup

class DpOrderService {
    static changeSingleOffer(resource: string, data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.post(API_URL + [resource, 'rejectOffer'].join('/'), data)
                .then(response => {
                    if (response.data.response) {
                        resolve(response.data);
                    } else {
                        reject();
                    }
                })
                .catch(error => {
                    reject(error);
                });
        });
    }

    static changeMultiOffer(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            // Implement your logic here based on the specific requirements
            // This is a placeholder implementation
            axios.post(API_URL + '/some/resource/multiOffer', data)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

export default DpOrderService;