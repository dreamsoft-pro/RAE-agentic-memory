import api from '@/lib/api';

class DataFetcher {
    private position: number;
    private document: Document; // Assuming this is related to a DOM element in JS context.
    private offsetParent: HTMLElement;
    private scrollParent: HTMLElement;
    private cssPosition: string;

    constructor(position?: number) {
        if (position !== undefined) {
            this.position = position;
        } else {
            this.position = 0; // Default value, adjust as needed
        }
        this.document = document; // Example initialization for the sake of completion.
        this.offsetParent = document.body;
        this.scrollParent = document.body;
        this.cssPosition = 'absolute';
    }

    async fetchData(d: string): Promise<void> {
        const pos = this.position || 0; // Ensure position is defined and defaults to 0 if not provided
        let mod: number, scroll: HTMLElement, scrollIsRootNode: boolean;

        if (d === "absolute") {
            mod = 1;
        } else {
            mod = -1;
        }

        const shouldUseOffsetParent = this.cssPosition === 'absolute' &&
            !(this.scrollParent !== this.document.body && this.scrollParent.contains(this.offsetParent));
        
        scroll = shouldUseOffsetParent ? this.offsetParent : this.scrollParent;

        scrollIsRootNode = /(html|body)/i.test(scroll.tagName);

        // Example API call using the imported api module
        try {
            const response = await api.get('/some-endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    }

    private contains(parent: HTMLElement, child: HTMLElement): boolean {
        return parent.contains(child);
    }
}

// Usage example
const dataFetcher = new DataFetcher();
dataFetcher.fetchData("absolute");