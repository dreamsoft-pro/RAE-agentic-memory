import api from "@/lib/api";

interface LangSettings {
  // Define the structure of your lang settings here based on what's expected
}

export default class LangSettingsRootService {

    private resource: string;
    private url: string;

    constructor(resource?: string, url?: string) {
        this.resource = resource ?? 'defaultResource'; // Default value or pass as a parameter
        this.url = url ?? '/api/langsettings'; // Default value or pass as a parameter
    }

    public async getLangSettings(): Promise<LangSettings> {
        try {
            const response = await api.get(this.url, { params: { resource: this.resource } });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch lang settings for resource ${this.resource}: ${error}`);
        }
    }

}

// Example usage in a component or somewhere else
const service = new LangSettingsRootService('en', '/api/custom-lang');
service.getLangSettings().then(settings => console.log(settings));