import api from '@/lib/api';
import { useEffect, useRef } from 'react';

class TabsComponent {
    private running: boolean;
    private active: any;
    private xhr?: any;

    constructor(private options: any) {}

    public activateTab(tab: HTMLElement, event: Event): void {
        if (
            tab.classList.contains("ui-state-disabled") ||
            // tab is already loading
            tab.classList.contains("ui-tabs-loading") ||
            // can't switch during an animation
            this.running ||
            // click on active header, but not collapsible
            (tab === this.active && !this.options.collapsible) ||
            // allow canceling activation
            (!this._trigger("beforeActivate", event))
        ) {
            return;
        }

        const collapsing = tab.classList.contains("ui-state-collapsing");
        this.options.active = collapsing ? false : this.tabs.index(tab);

        this.active = tab === this.active ? document.createElement('div') : tab;
        if (this.xhr) {
            this.xhr.abort();
        }

        const toHide: HTMLElement[] = [];
        const toShow: HTMLElement[] = [];

        // Assuming you need to set these variables based on some logic
        // For example, let's assume `toHide` and `toShow` are derived from eventData passed into _toggle

        if (!toHide.length && !toShow.length) {
            throw new Error("jQuery UI Tabs: Mismatching fragment identifier.");
        }

        if (toShow.length) {
            this.load(this.tabs.index(tab), event);
        }
        this._toggle(event, { newPanel: toShow[0], oldPanel: toHide[0] });
    }

    private _toggle(event: Event, eventData: any): void {
        const that = this;
        const toShow = eventData.newPanel;
        const toHide = eventData.oldPanel;

        useEffect(() => {
            that.running = true;
            // Logic for show/hide panels here
            setTimeout(() => (that.running = false), 1000); // Example delay
        }, []);
    }

    private _trigger(event: string, originalEvent?: Event): boolean | void {
        if (!this.options[event]) return; // Check for the event handler existence
        this.options[event](originalEvent);
    }

    private load(index: number, event: Event) {
        api.get(`/path/to/resource/${index}`)
            .then((response) => {
                const newPanel = document.createElement('div');
                newPanel.innerHTML = response.data;
                this._toggle(event, { newPanel });
            })
            .catch(() => {
                console.error("Failed to load tab content");
            });
    }
}