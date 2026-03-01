import api from "@/lib/api";

class PsPricelistService {

    static async edit(item: any): Promise<any> {
        try {
            const response = await api.put('ps_priceLists', item);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async remove(item: any): Promise<void> {
        try {
            await api.delete(`ps_priceLists/${item.id}`);
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default PsPricelistService;