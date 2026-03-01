import api from '@/lib/api';

class LangSettingsRootService {
    static update(lang: any, resource: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
        
        return api.post(url, lang)
            .then((data) => {
                if (data.response) {
                    // Assuming cache is a global or imported object
                    cache.remove('collection');
                    return data.item;
                } else {
                    throw data;
                }
            })
            .catch((error) => {
                throw error;
            });
    }
}