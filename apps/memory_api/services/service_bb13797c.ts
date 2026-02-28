import axios from 'axios';

class DpOrderService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    public saveCart(orderID: string, sendData: any): Promise<any> {
        return axios.patch(`${this.apiUrl}/${resource}/saveCart/${orderID}`, sendData).then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    public getMyZone(params?: Record<string, any>): Promise<any> {
        return axios.get(`${this.apiUrl}/${resource}/myZone`, { params: params || {} }).then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}