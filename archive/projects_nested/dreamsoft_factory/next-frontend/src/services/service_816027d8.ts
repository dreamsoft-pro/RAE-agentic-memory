import axios from 'axios';

class CanvasService {
    private static filters: Record<string, any> = {};

    public static async loadFilters(): Promise<void> {
        const response = await axios.get('https://api.example.com/filters');
        CanvasService.filters = response.data;
    }

    public static getFilter(name: string): any {
        return CanvasService.filters[name];
    }

    public static getFilters(): Record<string, any> {
        return CanvasService.filters;
    }
}

export default CanvasService;