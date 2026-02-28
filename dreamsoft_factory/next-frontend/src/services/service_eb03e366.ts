import axios from '@/lib/api';
import { useRouter } from 'next/router';

class MyClass {
    private resource: string[];
    private metaTag: any; // Replace `any` with the appropriate type if known.
    private routeID: number;

    constructor(resource: string[], metaTag: any, routeID: number) {
        this.resource = resource;
        this.metaTag = metaTag;
        this.routeID = routeID;
    }

    public async fetchData(): Promise<any> {
        try {
            const url = process.env.NEXT_PUBLIC_API_URL + this.resource.join('/');
            const response = await axios.post(url, {
                languages: this.metaTag.languages,
                routeID: this.routeID
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error; // Re-throw the error if needed.
        }
    }
}

export default MyClass;

// Usage example:
// const myClass = new MyClass(['path', 'to', 'resource'], { languages: ['en', 'fr'] }, 123);
// myClass.fetchData().then(data => console.log(data));