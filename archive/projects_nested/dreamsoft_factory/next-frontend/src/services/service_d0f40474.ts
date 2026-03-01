import api from '@/lib/api';
import { useState, useEffect } from 'react';

export default class TaxService {
    private resource: string = "taxes";

    remove(id: number): Promise<void> {
        return new Promise((resolve, reject) => {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${id}`;
            
            api.delete(url)
                .then(response => resolve())
                .catch(error => reject(error));
        });
    }

    getForProduct(groupID: number, typeID?: number): Promise<any> {
        return new Promise((resolve, reject) => {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
            let params = `?groupID=${groupID}`;

            if (typeID !== undefined) {
                params += `&typeID=${typeID}`;
            }

            api.get(url + params)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}