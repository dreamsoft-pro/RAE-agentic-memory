import api from '@/lib/api';

class DataFetcher {
    private resource: string = '/data'; // Example resource path

    constructor(private url?: string) {
        if (url !== undefined) this.resource = url;
    }

    public async fetchAndProcessData(): Promise<void> {
        try {
            const response = await api.get(this.resource);
            console.log(response.data); // Process the data as needed
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    }
}

// Usage in a Next.js page component or elsewhere
export default function MyPage() {
    const fetchData = new DataFetcher('/api/data');
    
    async function handleFetchDataOnClick() {
        await fetchData.fetchAndProcessData();
    }

    return (
        <button onClick={handleFetchDataOnClick}>Fetch Data</button>
    );
}