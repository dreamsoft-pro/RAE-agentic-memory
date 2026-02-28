import api from "@/lib/api";

class DraggableComponent {
    private helper?: any;
    private margins!: { top: number; left: number };
    private offset!: { top: number; left: number };

    constructor(private event: any, private currentItem: any) {}

    public initialize(): void {
        this.helper = this._createHelper(this.event);

        // Cache the helper size
        this._cacheHelperProportions();

        // Cache the margins of the original element
        this._cacheMargins();

        // Get the next scrolling parent
        const scrollParent = this.helper.scrollParent();

        // The element's absolute position on the page minus margins
        const offset = this.currentItem.offset();
        this.offset = {
            top: offset.top - this.margins.top,
            left: offset.left - this.margins.left
        };
    }

    private _createHelper(event: any): any {
        // Implementation for creating helper
        return {}; // Placeholder implementation
    }

    private async _cacheHelperProportions(): Promise<void> {
        // Implementation to cache the proportions of the helper element
    }

    private async _cacheMargins(): Promise<void> {
        const resource = "margins"; // Example resource name, replace with actual logic

        try {
            const response = await api.get(`/api/${resource}`);
            this.margins = response.data;
        } catch (error) {
            console.error(`Failed to fetch margins: ${error.message}`);
        }
    }
}