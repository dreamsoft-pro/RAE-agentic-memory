import api from '@/lib/api';
import { loadMargins, Notification } from './path-to-your-modules'; // Adjust path as necessary

class MarginFormController {
    selectedPriceListID: number;
    selectedNatureID: number;
    currentGroupID: number;

    async addMargin() {
        const data = JSON.parse(JSON.stringify(this.marginForm)); // Use deep clone instead of _
        data.priceTypeID = this.selectedPriceListID;
        data.natureID = this.selectedNatureID;
        data.groupID = this.currentGroupID;

        try {
            const response = await api.post('/api/margins', data);
            if (response.data.response) {
                Notification.success('success'); // Replace 'success' with actual success message key
                this.marginForm = {};
                loadMargins();
            } else {
                Notification.error('error'); // Replace 'error' with actual error message key
            }
        } catch (error) {
            Notification.error('error'); // Replace 'error' with actual error message key
        }
    }

    constructor() {
        this.selectedPriceListID = 0; // Example initial value, adjust accordingly
        this.selectedNatureID = 0; // Example initial value, adjust accordingly
        this.currentGroupID = 0; // Example initial value, adjust accordingly
    }
}

export default MarginFormController;