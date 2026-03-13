import React from 'react';
import { useRouter } from 'next/router';
import api from '@/lib/api'; // Assuming this is correctly set up in your project

class TabComponent extends React.Component {
    private active: any[] = []; // Example type; adjust based on actual structure of `active`
    private tabs: any[] = [];   // Example type; adjust based on actual structure of `tabs`
    private anchors: any[] = []; // Example type; adjust based on actual structure of `anchors`
    private xhr: any;

    constructor(props) {
        super(props);
        this._findActive = this._findActive.bind(this);
        this._getIndex = this._getIndex.bind(this);
        this._destroy = this._destroy.bind(this);
    }

    simulateClickOnCurrentHeader(active: any[]) {
        if (active.length === 0) {
            active = this.active;
        }
        
        const anchorElement = active.find(".ui-tabs-anchor")[0];
        this._eventHandler({
            target: anchorElement,
            currentTarget: anchorElement,
            preventDefault: () => {} // Equivalent to $.noop
        });
    }

    private _findActive(index?: number): any {
        return index === undefined ? [] : this.tabs.eq(index);
    }

    private async _getIndex(index: string | number): Promise<number> {
        if (typeof index === 'string') {
            const anchor = this.anchors.filter(`[href$='${index}']`)[0];
            index = this.anchors.index(anchor);
        }
        
        return index;
    }

    private _destroy() {
        if (this.xhr) {
            this.xhr.abort();
        }

        this.element && this.element.removeClass(
            "ui-tabs ui-widget ui-widget-content ui-corner-all ui-tabs-collapsible"
        );

        this.tablist?.removeClass(
            "ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all"
        ).removeAttr("role");
    }
}

export default TabComponent;