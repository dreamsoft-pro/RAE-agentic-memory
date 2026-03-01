import api from '@/lib/api';

class UploadService {
    private resourceGraphics = '/some-resource-path'; // Replace with actual path or define as needed

    getFaviconUploadUrl(): string {
        return `${this.resourceGraphics}/favicon`;
    }

    getModelFiles(): Promise<any> {
        const url = `${this.resourceGraphics}/modelIcon`;

        return api.get(url).then((response) => response.data)
            .catch((error) => {
                throw new Error(error);
            });
    }

    getUploader(url: string): any { // Replace 'any' with the appropriate type if known
        return new FileUploader({
            url,
            autoUpload: false,
            queueLimit: 1,
            removeAfterUpload: true
        });
    }
}