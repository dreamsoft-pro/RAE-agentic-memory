import api from '@/lib/api';

export default class AuctionService {
    private static async deleteResource(resource: string, id: number): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${resource}/${id}`;
            const response = await api.delete(url);

            if (response.data.response) {
                // Assuming cache is a global object that can be used to remove items.
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error('Response data does not contain "response" property');
            }
        } catch (error) {
            throw error;  // Re-throw the error to maintain consistency with the original code's rejection behavior
        }
    }

    public static async isAuctionUser(): Promise<any> {
        const def = { resolve: () => {}, reject: () => {} as ((reason?: any) => void) };

        try {
            // Perform some action that determines if the user is an auction user.
            // This is a placeholder for actual logic to determine whether the user is an auction user.
            // For example, you might make another API call or check some condition.

            def.resolve(true);  // Example: Assuming the user is always an auction user
        } catch (error) {
            def.reject(error);
        }

        return new Promise((resolve, reject) => {
            def.resolve = resolve;
            def.reject = reject;

            // Actual logic to determine if the user is an auction user would go here.
            // For this example, we're just resolving with true and rejecting in case of error.
            
            def.resolve(true);  // Placeholder resolve
        });
    }
}