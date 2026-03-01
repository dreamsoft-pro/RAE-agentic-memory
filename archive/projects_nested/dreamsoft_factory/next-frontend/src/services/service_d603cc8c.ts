import axios from 'axios';
import { useRouter } from 'next/router';

class PhotoFolderService {
    static getDomain(): string {
        const domainHost = this.getDomainHost();
        let port = window.location.port;
        if (port.length > 0) {
            return `${window.location.protocol}//${domainHost}:${port}`;
        }
        return `${window.location.protocol}//${domainHost}`;
    }

    private static getDomainHost(): string {
        // Implement logic to retrieve domain host, this is a placeholder
        return 'example.com';
    }

    static shareByEmail(photo: any, email: string): Promise<number> {
        const url = 'your-api-url-here'; // Define your API URL here
        const headers = {}; // Define your headers here

        const data = {
            email,
            host: this.getDomain(),
            lang: 'en' // Replace with logic to get current language code
        };

        return axios.post(url + 'folder/image/email-share/' + photo._id, data, { headers })
            .then((response) => response.status)
            .catch((error) => error.response ? error.response.status : 500);
    }

    static facebookShare(folder: any): Promise<void> {
        const def = this.defer();
        
        // Implement your Facebook share logic here
        // For now, we'll just resolve after a short delay to simulate an async operation
        setTimeout(() => def.resolve(), 1000);

        return def.promise;
    }

    private static defer(): { promise: Promise<void>; resolve: () => void; reject: (reason?: any) => void } {
        let resolve, reject;
        const promise = new Promise<void>((res, rej) => {
            resolve = res;
            reject = rej;
        });
        return { promise, resolve, reject };
    }
}

export default PhotoFolderService;