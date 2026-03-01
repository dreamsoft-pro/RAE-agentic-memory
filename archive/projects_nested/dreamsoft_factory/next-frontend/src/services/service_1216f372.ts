import api from '@/lib/api';
import { useState } from 'next/runtime'; // This import might be redundant if the function isn't directly related to React components

class DpShipmentService {
    static generateLabels(resource: string, packages: any[], orderID: number): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/generateLabels`;
        
        return api.patch(url, { packages, orderID })
            .then(response => response.data)
            .catch(error => {
                throw new Error(JSON.stringify(error.response?.data));
            });
    }

    static printLabel(shipmentID: number, orderAddressID: number): void | Promise<any> {
        // Assuming this function needs to use the generateLabels method or perform another async operation
        DpShipmentService.generateLabels('shipments', [], shipmentID)
            .then(data => console.log(data))
            .catch(error => console.error(error));
    }
}