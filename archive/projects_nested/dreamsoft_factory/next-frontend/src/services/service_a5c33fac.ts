import api from '@/lib/api';

export default class ConnectOptionService {
    static removePrice = async (price: any): Promise<any> => {
        console.log(price);

        try {
            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/price/${price.connectOptionID}?amount=${price.amount}`);

            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response does not contain required data');
            }
        } catch (error) {
            throw error; // Re-throw the error for handling in upper layers
        }
    };
}