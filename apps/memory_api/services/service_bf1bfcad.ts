import api from '@/lib/api';
import { Cache } from 'your-cache-module'; // Assuming you have a cache module or use localStorage/sessionStorage similarly

class PsPricelistService {
    static async delete(itemID: string) {
        try {
            const response = await api.delete(`/ps_priceLists/${itemID}`);
            
            if (response.data.response) {
                let collection = Cache.get('collection');
                let index = _.findIndex(collection, { ID: itemID });
                
                if (index !== -1) {
                    collection.splice(index, 1);
                    Cache.put('collection', collection);

                    // Assuming $rootScope.$emit is a custom event emitter
                    const emitEvent = () => this.emit('ps_priceLists', collection);
                    emitEvent();
                    
                    return collection;
                }
            }

            throw new Error("Failed to delete the item");
        } catch (error) {
            throw error;  // Re-throwing for clarity
        }
    }

    static async deleteIcon(priceListID: string) {
        const resourcePath = ['ps_priceLists', 'uploadIcon'];
        
        try {
            await api.delete(`${resourcePath.join('/')}/${priceListID}`);
            
            // Assuming similar cache logic is needed here as well
            let collection = Cache.get('collection');
            let index = _.findIndex(collection, { ID: priceListID });
            
            if (index !== -1) {
                collection.splice(index, 1);
                Cache.put('collection', collection);

                const emitEvent = () => this.emit('ps_priceLists', collection);
                emitEvent();

                return collection;
            }
        } catch (error) {
            throw error; // Re-throwing for clarity
        }
    }

    // Method to simulate $rootScope.$emit functionality
    static emit(eventName: string, data: any): void {
        console.log(`Emitting event ${eventName} with data`, data);
        // Implement your custom event emitter here if needed
    }
}