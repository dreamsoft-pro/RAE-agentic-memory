import api from '@/lib/api';
import { useEffect, useRef } from 'react';

class TabManager extends React.Component {
    private tabs: HTMLCollection;
    private panels: NodeListOf<Element>;
    private activeTabRef = useRef<HTMLLIElement>(null);

    componentDidMount() {
        this.tabs = document.querySelectorAll('.tab');
        this.panels = document.querySelectorAll('.tabpanel');

        this.applyTabAttributes();
    }

    applyTabAttributes() {
        // Apply attributes to inactive tabs
        Array.from(this.tabs).forEach((tab, index) => {
            if (!this.isActive(tab)) {
                tab.setAttribute('aria-selected', 'false');
                tab.setAttribute('aria-expanded', 'false');
                tab.tabIndex = -1;

                this.hidePanel(index);
            }
        });

        // Ensure at least one tab is focusable
        if (Array.from(this.tabs).every(tab => !this.isActive(tab))) {
            Array.from(this.tabs)[0].tabIndex = 0;
        } else {
            const activeTab = this.getActiveTab();
            if (activeTab) {
                activeTab.classList.add("ui-tabs-active", "ui-state-active");
                activeTab.setAttribute('aria-selected', 'true');
                activeTab.setAttribute('aria-expanded', 'true');
                activeTab.tabIndex = 0;

                // Show the panel associated with the selected tab
                this.showPanel(Array.from(this.tabs).indexOf(activeTab));
            }
        }
    }

    getActiveTab() {
        return Array.from(this.tabs).find(tab => this.isActive(tab));
    }

    hidePanel(index: number) {
        const panel = this.panels[index];
        if (panel) {
            panel.setAttribute('aria-hidden', 'true');
            // Additional logic to handle showing/hiding panels goes here
        }
    }

    showPanel(index: number) {
        const panel = this.panels[index];
        if (panel) {
            panel.setAttribute('aria-hidden', 'false');
            // Additional logic to handle showing/hiding panels goes here
        }
    }

    isActive(tab: HTMLLIElement): boolean {
        return tab.classList.contains("ui-tabs-active");
    }
}