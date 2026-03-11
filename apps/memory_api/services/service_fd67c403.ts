import axios from '@/lib/api';
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    // Ensure the variable is defined before use.
    const url = req.query.url as string;
    
    try {
        // Using native async/await and Axios.
        const response = await axios.get(url);
        
        // Return data from your API call
        res.status(200).json(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'An error occurred while fetching the data.' });
    }
}