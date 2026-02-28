import api from '@/lib/api';
import { AuctionResponse } from '@/types'; // Assuming there is a type definition for response

class AuctionService {
    private companyID: number;

    constructor(companyID: number) {
        this.companyID = companyID;
    }

    async editResponse(auctionID: number, response: Partial<AuctionResponse>): Promise<void> {
        try {
            const { realizationDate, description, items } = response;

            await api.put(`/auctions/${auctionID}/auctionResponses`, {
                companyID: this.companyID,
                realizationDate,
                description,
                items
            });

            // If needed, perform further operations here after successful PUT request

        } catch (error) {
            console.error('Error updating auction response:', error);
            throw error;  // Re-throw the error to handle it in calling context if necessary
        }
    }

    /**
     * Example usage:
     * const service = new AuctionService(12345); 
     * await service.editResponse(67890, { realizationDate: 'today', description: 'new desc', items: [{ itemID: 1, price: 123 }] });
     */
}