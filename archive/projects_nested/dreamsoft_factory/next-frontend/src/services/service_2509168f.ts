import React, { Component } from 'react';
import axios from '@/lib/api'; // Assuming this is a custom API wrapper using Axios

interface TabProps {
  index: number;
}

class TabManager extends Component<TabProps> {
  private tabs: HTMLElement[] = [];
  private activeTab: HTMLElement | null = null;

  componentDidMount() {
    this.tabs = document.querySelectorAll('.tab'); // Example selector for simplicity
    if (this.tabs.length) {
      this.activeTab = this.tabs[0]; // Set initial active tab, adjust as necessary
    }
  }

  async switchTabs(newIndex: number) {
    const toShow = this.tabs[newIndex];
    let toHide = this.activeTab;

    // Hide the old tab and update attributes
    if (toHide) {
      toHide.setAttribute('aria-hidden', 'true');
      toHide.setAttribute('aria-selected', 'false');
      toHide.setAttribute('aria-expanded', 'false');

      // Adjust tab order
      if (toShow && this.tabs.length > 1) {
        toHide.setAttribute('tabIndex', '-1');
      } else if (toShow) {
        const activeTabs = Array.from(document.querySelectorAll('.tab[tabindex="0"]'));
        activeTabs.forEach(tab => tab.setAttribute('tabIndex', '-1'));
      }
    }

    // Show the new tab and update attributes
    toShow?.setAttribute('aria-hidden', 'false');
    toShow?.setAttribute('aria-selected', 'true');
    toShow?.setAttribute('tabIndex', '0');

    this.activeTab = toShow;
  }

  async activate(index: number) {
    const activeElement = this.tabs[index];
    
    if (this.activeTab && this.activeTab === activeElement) return;

    await this.switchTabs(index);
  }

  render() {
    // Render logic can go here
    return <div className="tab-container">{/* JSX elements */}</div>;
  }
}

export default TabManager;