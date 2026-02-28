import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {
    private static API_URL: string = process.env.API_URL || '';

    public static acceptOffer(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.post(`${this.API_URL}/${resource}/acceptOffer`, data)
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

    public static rejectOffer(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.post(`${this.API_URL}/${resource}/rejectOffer`, data)
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
}