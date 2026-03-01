import axios from 'axios';

class UserAddressService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL;
    }

    public async edit(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.post(this.apiUrl + this.resource, data)
                .then(response => {
                    if (response.data.response) {
                        resolve(response.data);
                    } else {
                        reject(response.data);
                    }
                })
                .catch(error => {
                    reject(error.response?.data ?? error);
                });
        });
    }

    private get resource(): string {
        return 'your-resource-endpoint'; // Replace with your actual endpoint
    }
}