import api from '@/lib/api';

class HelpersService {
    static async showImposition(workspace: any, formatWidth: number, formatHeight: number, targetID: string): Promise<void> {
        const canvasSize = 600;
        const elementId = `canva-${targetID}`;
        
        // Ensure the canvas is defined before use
        const c = document.getElementById(elementId) as HTMLCanvasElement;

        if (!c) {
            console.error(`Element with id '${elementId}' not found.`);
            return;
        }

        c.width = c.height = canvasSize;
        c.style.display = c.style.display === 'none' ? 'block' : 'none';

        const drawing = c.style.display === 'block';
        
        if (drawing) {
            const scale = 1 / Math.max(workspace.width / canvasSize, workspace.height / canvasSize);
            const aResult = workspace.areaPerSheetForStandardResult;

            // Example usage of the imported API
            try {
                const response = await api.get('/some-endpoint');
                console.log(response.data);
            } catch (error) {
                console.error('API request failed:', error);
            }
        }
    }
}

// Usage example:
HelpersService.showImposition({ width: 100, height: 200 }, 567, 890, 'targetCanvas').catch(console.error);