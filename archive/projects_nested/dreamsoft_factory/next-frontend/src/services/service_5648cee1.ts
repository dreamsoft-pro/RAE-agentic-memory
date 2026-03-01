import api from '@/lib/api';

export default class DataFetcher {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async fetchData(): Promise<void> {
        try {
            const response = await api.get(this.url);
            console.log(`${this.resource} data fetched successfully`);
            // Process the response here
        } catch (error) {
            console.error(`Failed to fetch ${this.resource} data:`, error);
        }
    }

    _cacheMargins(): void {
        this.margins = {
            left: parseInt(this.currentItem.css("marginLeft"), 10) || 0,
            top: parseInt(this.currentItem.css("marginTop"), 10) || 0
        };
    }

    _cacheHelperProportions(): void {
        this.helperProportions = {
            width: this.helper.outerWidth(),
            height: this.helper.outerHeight()
        };
    }
}