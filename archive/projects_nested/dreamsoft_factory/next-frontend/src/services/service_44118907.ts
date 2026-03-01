import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

class CanvasService {
    private canvas: HTMLCanvasElement | null = null;
    private context: CanvasRenderingContext2D | null = null;
    private stage: any; // Replace `any` with the actual type if known
    private bitmap: any; // Replace `any` with the actual type if known
    private filters: Record<string, any> = {};

    setCanvas(newCanvas: HTMLCanvasElement): void {
        this.canvas = newCanvas;
    }

    setContext(newContext: CanvasRenderingContext2D): void {
        this.context = newContext;
    }

    getCanvas(): HTMLCanvasElement | null {
        return this.canvas;
    }

    getContext(): CanvasRenderingContext2D | null {
        return this.context;
    }

    setStage(newStage: any): void { // Replace `any` with the actual type if known
        this.stage = newStage;
    }

    getStage(): any { // Replace `any` with the actual type if known
        return this.stage;
    }

    setBitmap(newBitamp: any): void { // Replace `any` with the actual type if known
        this.bitmap = newBitamp;
    }
}

export default CanvasService;

// Example usage in a Next.js API route (if needed)
export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const canvasService = new CanvasService();
    
    // Use axios for HTTP requests if necessary
    axios.get('https://api.example.com/data')
        .then(response => {
            console.log(response.data);
            res.status(200).json({ message: 'Data fetched successfully' });
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({ error: 'Failed to fetch data' });
        });
}