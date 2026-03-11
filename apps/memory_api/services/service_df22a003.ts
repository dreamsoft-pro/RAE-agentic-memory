import api from '@/lib/api';
import { CARTS_ADD_URL } from '@/constants'; // Assuming you have a constant file for URLs

class DpCartsDataService {
    private url = CARTS_ADD_URL; // Ensure this is defined based on your application's structure

    async add(addData: any) {
        try {
            const response = await api.post(this.url, addData);
            window.dispatchEvent(new CustomEvent('Cart:copied', { detail: true }));
        } catch {
            Notification.error('error'); // Assuming 'Notification' is a global or imported service
        }
    }

    async addToCart(data: any) {
        try {
            const cartsData = await api.post(this.url, data); // Adjust the URL if needed for this specific call
            window.dispatchEvent(new CustomEvent('Cart:copied', { detail: true }));
        } catch {
            Notification.error('error'); // Assuming 'Notification' is a global or imported service
        }
    }
}

const dpCartsDataService = new DpCartsDataService();

async function handleAddToCart(addData?: any, data?: any) {
    if (addData) {
        await dpCartsDataService.add(addData);
    } else if (data) {
        await dpCartsDataService.addToCart(data);
    }
}