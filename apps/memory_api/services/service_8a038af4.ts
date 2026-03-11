import api from '@/lib/api';

class LangSettingsService {
    private resource: string;

    constructor() {
        this.resource = 'settings/lang';
    }

    public async getLangSettings(): Promise<string[]> {
        try {
            const url = `${this.resource}/current`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch lang settings:', error);
            throw new Error('Unable to retrieve language settings');
        }
    }

    public async updateLangSettings(settings: string[]): Promise<void> {
        try {
            const url = `${this.resource}/update`;
            await api.put(url, { data: settings });
        } catch (error) {
            console.error('Failed to update lang settings:', error);
            throw new Error('Unable to update language settings');
        }
    }

    public async deleteLangSettings(): Promise<void> {
        try {
            const url = `${this.resource}/delete`;
            await api.delete(url);
        } catch (error) {
            console.error('Failed to delete lang settings:', error);
            throw new Error('Unable to delete language settings');
        }
    }
}

export default LangSettingsService;