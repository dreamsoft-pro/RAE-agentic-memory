import api from "@/lib/api";

AuctionService.prototype.create = async function (resource: string, auctionID: string | number, response: any): Promise<any> {
    const url = `${process.env.API_URL}/${[resource, auctionID, 'auctionResponses'].join('/')}`;

    try {
        const data = await api.put(url, response);
        if (data.response) {
            return data;
        } else {
            throw new Error(JSON.stringify(data));
        }
    } catch (error) {
        return Promise.reject(error);
    }
};