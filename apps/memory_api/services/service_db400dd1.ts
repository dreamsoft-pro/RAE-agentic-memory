import api from '@/lib/api';
import { createDeferred } from 'your-deferred-helper'; // Assuming a helper to create deferred objects

class LangSettingsRootService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(lang: any): Promise<any> {
        const { resolve, reject } = createDeferred();

        try {
            const response = await api.put(this.getUrlForUpdate(), lang);
            if (response.data.response) {
                resolve(response.data);
            } else {
                reject(response.data);
            }
        } catch (error) {
            reject(error);
        }

        return resolve.promise;
    }

    async remove(id: string): Promise<any> {
        const { resolve, reject } = createDeferred();

        try {
            const response = await api.delete(this.getUrlForRemove(id));
            if (response.data.response) {
                resolve(response.data);
            } else {
                reject(response.data);
            }
        } catch (error) {
            reject(error);
        }

        return resolve.promise;
    }

    private getUrlForUpdate(): string {
        return `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
    }

    private getUrlForRemove(id: string): string {
        return `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${id}`;
    }
}