import React from 'react';
import api from '@/lib/api'; // Assuming this is the correct import path for axios replacement

class TabsComponent extends React.Component {
    private element: HTMLElement;
    private options: any; // Replace `any` with proper type definition if known
    private anchors: HTMLAnchorElement[] = [];
    private active?: React.ReactElement | null;

    public running = false;

    private _processTabs(): void {
        // Implement logic to process tabs
    }

    private _initialActive(): number {
        // Implement logic to find initial active tab index
        return 0; // Dummy value, replace with actual implementation
    }

    private _findActive(index: number | null): React.ReactElement[] | null {
        if (index === undefined || index === -1) {
            return [];
        }
        const $tabs = this.anchors;
        let activeAnchor: HTMLAnchorElement;

        if (typeof index === 'number') { // 0-based indexing
            activeAnchor = $tabs[index];
        } else {
            // Handle string or other types of `index`
            // Assuming logic to find the correct anchor element based on index value
            return [];
        }

        if (activeAnchor) {
            this.anchors.forEach((anchor, i) => {
                const selected: boolean = anchor === activeAnchor;
                $(this.tabs[i]).attr('aria-selected', selected ? 'true' : 'false');
                anchor.tabIndex = -1; // Prevent click-paste in IE #6827
            });
        }

        return [activeAnchor];
    }

    private _refresh(): void {
        this._setupDisabled();
        this._setupMouseids();
        this._markActive();
        this._createHelper();
    }

    private _initialActivate(): void {
        if (this.active) {
            // Activate the active tab
        }
    }

    public async load(active: number): Promise<void> {
        try {
            const content = await api.get(`/api/tabs/${active}`); // Replace with actual API endpoint
            console.log(content);
            this.setState({ content });
        } catch (error) {
            console.error('Failed to load tab content:', error);
        }
    }

    public create(): void {
        let that = this;
        const options = this.options;

        this.running = false;

        if (this.element instanceof HTMLElement) {
            this.element
                .classList.add("ui-tabs", "ui-widget", "ui-widget-content", "ui-corner-all")
                .classList.toggle("ui-tabs-collapsible", options.collapsible);
        }

        this._processTabs();
        options.active = this._initialActive();

        if (Array.isArray(options.disabled)) {
            const disabledIndexes: number[] = $.unique(
                options.disabled.concat($.map(this.tabs.filter(".ui-state-disabled"), function(li) { 
                    return that.tabs.index(li); 
                }))
            ).sort();
            options.disabled = disabledIndexes;
        }

        if ((this.options.active !== false && this.anchors.length)) {
            this.active = this._findActive(options.active);
        } else {
            this.active = null;
        }

        this._refresh();

        if (this.active) {
            this.load(options.active as number);
        }
    }
}

export default TabsComponent;