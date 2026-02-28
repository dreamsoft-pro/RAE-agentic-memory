import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface ReclamationService {
    getMessages: (reclamationID: string) => Promise<any>;
    getFiles: (reclamationID: string) => Promise<any>;
}

const API_URL = process.env.API_URL; // Ensure you have this environment variable set

export const ReclamationService: ReclamationService = {
    async getMessages(reclamationID: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/${messagesResource}/myZone/${reclamationID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to fetch messages');
        }
    },

    async getFiles(reclamationID: string): Promise<any> {
        try {
            const response = await axios.get(`${API_URL}/${resource}/getFiles/${reclamationID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to fetch files');
        }
    },
};