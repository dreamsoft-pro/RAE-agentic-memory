import api from '@/lib/api';
import { useEffect } from 'next/react';

class TabManager {
    private anchors: NodeListOf<Element>;
    private tablist: HTMLElement;
    private tabs: NodeListOf<Element>;
    private panels: NodeListOf<Element>;

    constructor(anchorSelector: string, tabListId: string) {
        this.anchors = document.querySelectorAll(anchorSelector);
        this.tablist = document.getElementById(tabListId) as HTMLElement;
        this.tabs = document.querySelectorAll('.tabs');
        this.panels = document.querySelectorAll('.panels');
    }

    async destroy() {
        // Remove class and attributes from anchors
        for (const anchor of this.anchors) {
            if (anchor.classList.contains('ui-tabs-anchor')) {
                anchor.classList.remove('ui-tabs-anchor');
                anchor.removeAttribute('role');
                anchor.removeAttribute('tabIndex');
                anchor.removeAttribute('uniqueId');  // assuming removeUniqueId is to remove a unique id attribute
            }
        }

        // Unbind events from tablist (assuming this means removing event listeners)
        this.tablist.removeEventListener(this.eventNamespace, () => {});  // Simplified example

        // Iterate through tabs and panels
        for (const tab of this.tabs) {
            if (tab.dataset['ui-tabs-destroy'] === 'true') {
                tab.remove();
            } else {
                tab.classList.remove(
                    'ui-state-default',
                    'ui-state-active',
                    'ui-state-disabled',
                    'ui-corner-top',
                    'ui-corner-bottom',
                    'ui-widget-content',
                    'ui-tabs-active',
                    'ui-tabs-panel'
                );
                tab.removeAttribute('tabIndex');
                tab.removeAttribute('ariaLive');  // Assuming aria-live is the attribute name
                tab.removeAttribute('ariaBusy');  // Assuming aria-busy is the attribute name
                tab.removeAttribute('ariaSelected');  // Assuming aria-selected is the attribute name
                tab.removeAttribute('ariaLabelledBy');  // Assuming aria-labelledby is the attribute name
                tab.removeAttribute('ariaHidden');  // Assuming aria-hidden is the attribute name
                tab.removeAttribute('ariaExpanded');  // Assuming aria-expanded is the attribute name
                tab.removeAttribute('role');
            }
        }

        for (const panel of this.panels) {
            if (panel.dataset['ui-tabs-destroy'] === 'true') {
                panel.remove();
            } else {
                panel.classList.remove(
                    'ui-state-default',
                    'ui-state-active',
                    'ui-state-disabled',
                    'ui-corner-top',
                    'ui-corner-bottom',
                    'ui-widget-content',
                    'ui-tabs-active',
                    'ui-tabs-panel'
                );
                panel.removeAttribute('tabIndex');
                panel.removeAttribute('ariaLive');  // Assuming aria-live is the attribute name
                panel.removeAttribute('ariaBusy');  // Assuming aria-busy is the attribute name
                panel.removeAttribute('ariaSelected');  // Assuming aria-selected is the attribute name
                panel.removeAttribute('ariaLabelledBy');  // Assuming aria-labelledby is the attribute name
                panel.removeAttribute('ariaHidden');  // Assuming aria-hidden is the attribute name
                panel.removeAttribute('ariaExpanded');  // Assuming aria-expanded is the attribute name
                panel.removeAttribute('role');
            }
        }
    }

    private get eventNamespace(): string {
        return 'ui-tabs';
    }
}

export default TabManager;