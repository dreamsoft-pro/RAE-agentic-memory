import api from '@/lib/api';

class MetaTagService {
    private uploadResource: string[] = [];

    constructor() {
        this.uploadResource.push('uploadImage');
    }

    public async removeImage(lang: string, imageID: string): Promise<void> {
        const rs = this.uploadResource.join('/');
        console.log('remove url', rs);

        try {
            await api.delete(`${rs}/${lang}/${imageID}`);
        } catch (error) {
            throw error;
        }
    }
}

export default MetaTagService;