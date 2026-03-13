import axios from 'axios';
import { useState, useEffect } from 'react';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export class DomainService {
    static async updateDomain(resource: string, domain: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.put(`${apiUrl}/${resource}`, domain)
                .then(response => {
                    if (response.data.response) {
                        // Assuming cache.remove and event emitting are handled elsewhere in the context of Next.js
                        window.dispatchEvent(new CustomEvent('Domain:editSuccess'));
                        resolve(response.data);
                    } else {
                        reject(response.data);
                    }
                })
                .catch(error => {
                    reject(error);
                });
        });
    }

    static getCurrentDomain(): Promise<any> {
        return new Promise((resolve) => {
            DomainService.getAll().then(data => {
                const result = data.find(item => item.selected === 1);
                resolve(result);
            });
        });
    }
}