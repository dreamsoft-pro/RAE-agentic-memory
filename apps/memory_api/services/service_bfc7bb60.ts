import api from '@/lib/api';

class PsConfigPaperPrice {
    resource: string = 'papers'; // Assuming this is how you define the resource

    async remove(id: number): Promise<any> {
        try {
            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${id}`);
            
            if (response.data.response) {
                // Assuming cache.remove() exists and works as expected
                this.cacheRemove(this.resource);
                return response.data;
            } else {
                throw new Error('Data not successfully deleted');
            }
        } catch (error: any) {
            throw error;
        }
    }

    private cacheRemove(resource: string): void {
        // Implement the logic for removing from cache
        console.log(`${resource} removed from cache`);
    }
}

export default PsConfigPaperPrice;