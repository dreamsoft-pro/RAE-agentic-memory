// helpers.ts

import api from '@/lib/api'; // Assuming this is correctly set up elsewhere.

class Helpers {
    public static formatNumber(theNumber: number, precision: number): string {
        return theNumber.toFixed(precision);
    }

    public static putLabel(canvasCtx: CanvasRenderingContext2D, value: number | string, x: number, y: number, rotation?: number, color: string = '#000000'): void {
        canvasCtx.save();
        if (rotation !== undefined) {
            canvasCtx.translate(x, y);
            canvasCtx.rotate(rotation);
            x = 0;
            y = 0;
        }
        // Assuming drawText is a custom method or needs to be implemented
        // for now just showing how you might call it.
        Helpers.drawText(canvasCtx, value.toString(), x, y, color);
        if (rotation !== undefined) {
            canvasCtx.restore();
        }
    }

    public static drawText(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, color: string): void {
        ctx.font = '14px Arial';
        ctx.fillStyle = color;
        ctx.fillText(text, x, y);
    }

    // If you need to define more methods or async operations with api
    public static async fetchResource(resourceName: string) {
        try {
            const response = await api.get(`resource/${resourceName}`);
            return response.data; // Adjust based on actual API response structure.
        } catch (error) {
            console.error('Fetching resource failed:', error);
            throw error;
        }
    }

}

export default Helpers;

// Example usage in a component or another file:
import { useEffect, useState } from 'react';
import Helpers from './helpers';

const MyComponent: React.FC = () => {
    const [resourceData, setResourceData] = useState<any>(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await Helpers.fetchResource('example');
                setResourceData(data);
            } catch (error) {
                console.error(error);
            }
        }

        fetchData();
    }, []);

    return (
        <div>
            {/* Component JSX */}
        </div>
    );
};

export default MyComponent;