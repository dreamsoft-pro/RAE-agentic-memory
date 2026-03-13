import api from '@/lib/api';

class TabLoader {
    private _isLocal(anchor: string[]): boolean {
        // implementation of is local check logic
        return false; // example return value
    }

    private _ajaxSettings(anchor: string[], event: Event, eventData: any): object {
        // implementation of ajax settings generation
        return {}; // example return value
    }

    public async loadTab(anchor: string[], event: Event, eventData: any, complete: Function) {
        if (this._isLocal(anchor[0])) {
            return;
        }

        try {
            const response = await api.post(this._ajaxSettings(anchor, event, eventData));

            if (!response.statusText || response.statusText !== "canceled") {
                // Assuming panel and tab are accessible instances of UI elements
                tab.addClass("ui-tabs-loading");
                panel.attr("aria-busy", "true");

                setTimeout(() => {
                    panel.html(response.data);
                    this._trigger("load", event, eventData);

                    complete(response, 'success');
                }, 1);
            }
        } catch (error) {
            setTimeout(() => {
                complete(error.response || error.message, 'error');
            }, 1);
        }
    }

    private _trigger(eventType: string, event: Event, eventData: any): void {
        // implementation of trigger logic
    }
}