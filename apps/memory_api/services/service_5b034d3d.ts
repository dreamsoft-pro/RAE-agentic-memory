import api from "@/lib/api";

export default class TabsController {
    private options: { disabled?: boolean | number[] };
    private tabs: any; // Assuming this refers to a jQuery-like object containing tab elements.
    private panels: any; // Assuming this refers to a jQuery-like object containing panel elements.
    private xhr?: any;

    constructor(options: { disabled?: boolean | number[] }, tabs: any, panels: any) {
        this.options = options;
        this.tabs = tabs;
        this.panels = panels;
    }

    public disable(index?: number): void {
        let disabled = this.options.disabled ?? false;
        if (disabled === true) return;

        if (index === undefined) {
            disabled = true;
        } else {
            index = this._getIndex(index);
            if (this._isDisabled(index)) return;

            if ($.isArray(disabled)) {
                disabled = $.merge([index], disabled).sort();
            } else {
                disabled = [index];
            }
        }

        this._setupDisabled(disabled);
    }

    public async load(index: number, event?: Event): Promise<void> {
        index = this._getIndex(index);
        const that = this;
        const tab = this.tabs.eq(index);
        const anchor = tab.find(".ui-tabs-anchor");
        const panel = this._getPanelForTab(tab);

        try {
            tab.addClass("ui-tabs-loading");
            panel.attr("aria-busy", "true");

            await api.get(anchor.attr("href"));
            // Handle loading logic here, possibly update the DOM with new content.

        } catch (error) {
            console.error('Failed to load content:', error);
        }

        const complete = (jqXHR: any, status: string): void => {
            if (status === "abort") {
                that.panels.stop(false, true);
            }

            tab.removeClass("ui-tabs-loading");
            panel.removeAttr("aria-busy");

            if (jqXHR === that.xhr) {
                delete that.xhr;
            }
        };

        // Assuming api.get returns a Promise and completes with the complete handler.
    }

    private _getIndex(index: number): number {
        // Implementation for getting the correct index
        return index; // Placeholder implementation
    }

    private _isDisabled(index: number): boolean {
        const disabled = this.options.disabled ?? [];
        if ($.isArray(disabled)) {
            return $.inArray(index, disabled) !== -1;
        }
        return false;
    }

    private _setupDisabled(disabled: any[]): void {
        // Logic to set up the disabled state
    }

    private _getPanelForTab(tab: any): any {
        // Implementation for getting the panel associated with a tab
        return this.panels.eq(this.tabs.index(tab)); // Placeholder implementation
    }
}