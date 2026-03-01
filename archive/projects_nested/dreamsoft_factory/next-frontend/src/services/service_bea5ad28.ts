import { useState, useEffect } from 'react';
import axios from 'axios';
import api from '@/lib/api';

class CalcFileService {
    private static async setCollectionToSepia(setID: string): Promise<void> {
        const url = `${api.API_URL}/calcFilesUploader/setCollectionToSepia/${setID}`;
        try {
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    private static async removeCollectionFilters(setID: string): Promise<void> {
        const url = `${api.API_URL}/calcFilesUploader/removeCollectionFilters/${setID}`;
        try {
            const response = await axios.post(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    // Example usage within a React component
    static async useSetCollectionToSepia(setID: string): Promise<void> {
        try {
            const data = await this.setCollectionToSepia(setID);
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    static async useRemoveCollectionFilters(setID: string): Promise<void> {
        try {
            const data = await this.removeCollectionFilters(setID);
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

export default CalcFileService;