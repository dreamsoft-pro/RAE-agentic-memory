import api from '@/lib/api';

class GroupService {

    static async remove(item: { details: { ID: string } }) {
        try {
            const response = await api.delete(`/ps_groups/${item.details.ID}`);
            return Promise.resolve(response);
        } catch (error) {
            return Promise.reject(error.response ? error : error.response);
        }
    }

    static async getOneByID(ID: string): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/ps_groups/getOneByID/${ID}`;
            const response = await api.get(url);
            return Promise.resolve(response.data);  // Assuming the API returns data as a property of the response object
        } catch (error) {
            return Promise.reject(error.response ? error : error.response);
        }
    }

}

export default GroupService;