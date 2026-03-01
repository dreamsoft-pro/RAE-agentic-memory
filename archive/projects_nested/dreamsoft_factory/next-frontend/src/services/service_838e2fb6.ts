import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

class DataFetcher {
    private apiUrl = 'https://api.example.com'; // Replace with your API URL

    getProjects = async () => axios.get(`${this.apiUrl}/projects`);
    getPageSizeSelect = async (size: number) => axios.get(`${this.apiUrl}/pageSize`, { params: { size } });
    getPagingSettings = async (page: number, pageSize: number) => axios.get(`${this.apiUrl}/paging`, { params: { page, pageSize } });
    getOrders = async () => axios.get(`${this.apiUrl}/orders`);
    getStatuses = async () => axios.get(`${this.apiUrl}/statuses`);
    countOrders = async () => axios.get(`${this.apiUrl}/orderCount`);
    getDeliveries = async () => axios.get(`${this.apiUrl}/deliveries`);
    getAddress = async (id: string) => axios.get(`${this.apiUrl}/address/${id}`);
    getCommonData = async () => axios.get(`${this.apiUrl}/commonData`);
    addParam = async (paramName: string, paramValue: any) => axios.post(`${this.apiUrl}/params`, { paramName, paramValue });
    clearParams = async () => axios.delete(`${this.apiUrl}/params`);
    getFiles = async () => axios.get(`${this.apiUrl}/files`);
    getAggregateOrders = async () => axios.get(`${this.apiUrl}/aggregateOrders`);
    getAllFiles = async (folderId: string) => axios.get(`${this.apiUrl}/allFiles/${folderId}`);
    removeFile = async (fileId: string) => axios.delete(`${this.apiUrl}/file/${fileId}`);
    mergeFiles = async (sourceFileIds: string[], destinationFolderId: string) => axios.post(`${this.apiUrl}/merge`, { sourceFileIds, destinationFolderId });
    getPayments = async () => axios.get(`${this.apiUrl}/payments`);
    payment = async (data: any) => axios.post(`${this.apiUrl}/payment`, data);
    getDeliveryPrice = async (orderId: number) => axios.get(`${this.apiUrl}/deliveryPrice/${orderId}`);
    preparePrice = async (orderId: number, deliveryMethodId: number) => axios.post(`${this.apiUrl}/preparePrice`, { orderId, deliveryMethodId });
    getReclamationSettings = async () => axios.get(`${this.apiUrl}/reclamations`);
    orderMessages = async (messageData: any) => axios.post(`${this.apiUrl}/orderMessages`, messageData);
    orderMessageInfo = async (orderId: number) => axios.get(`${this.apiUrl}/orderMessage/${orderId}`);
    offerMessageInfo = async (offerId: string, messageId: number) => axios.get(`${this.apiUrl}/offerMessage/${offerId}/${messageId}`);
    doPayment = async (data: any) => axios.post(`${this.apiUrl}/doPayment`, data);
    acceptReport = async (reportId: string) => axios.post(`${this.apiUrl}/acceptReport/${reportId}`);
    rejectReport = async (reportId: string) => axios.post(`${this.apiUrl}/rejectReport/${reportId}`);

    // Example of how to use this class in a Next.js API route
    static getHandler() {
        return async (req: NextApiRequest, res: NextApiResponse) => {
            const dataFetcher = new DataFetcher();
            try {
                switch (req.method) {
                    case 'GET':
                        const { method } = req.query;
                        if (method === 'getProjects') await res.json(await dataFetcher.getProjects());
                        else if (method === 'getStatuses') await res.json(await dataFetcher.getStatuses());
                        // Add other methods here
                        break;
                    default:
                        res.setHeader('Allow', ['GET']);
                        res.status(405).end(`Method ${req.method} Not Allowed`);
                }
            } catch (err) {
                console.error(err);
                res.status(500).json({ error: 'Internal Server Error' });
            }
        };
    }
}

export default DataFetcher;