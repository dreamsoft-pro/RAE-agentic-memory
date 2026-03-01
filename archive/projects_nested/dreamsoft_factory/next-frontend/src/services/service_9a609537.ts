import api from "@/lib/api";
import $ from "jquery"; // Assuming you're using jQuery and it needs to be imported

export default class TabsComponent {
  private options: { active?: number | null; collapsible?: boolean };
  private tabs: JQuery;

  constructor(options: Partial<{ active?: number | null; collapsible?: boolean }>, tabs: JQuery) {
    this.options = {
      active: options.active,
      collapsible: Boolean(options.collapsible)
    };
    this.tabs = tabs;
  }

  async initialActive(): Promise<number | false> {
    const { active, collapsible } = this.options;
    let locationHash = window.location.hash.substring(1);

    if (active === null) {
      // check the fragment identifier in the URL
      if (locationHash) {
        for (let i = 0; i < this.tabs.length; i++) {
          const tab = $(this.tabs[i]);
          if (tab.attr("aria-controls") === locationHash) {
            active = i;
            break;
          }
        }
      }

      // check for a tab marked active via a class
      if (active === null) {
        const index = this.tabs.index(this.tabs.filter(".ui-tabs-active"));
        active = index !== -1 ? index : undefined;
      }

      // no active tab, set to false
      if (active === null || active === -1) {
        active = this.tabs.length ? 0 : false;
      }
    }

    // handle numbers: negative, out of range
    if (active !== false) {
      const index = this.tabs.index(this.tabs.eq(active));
      active = index === -1 ? collapsible ? false : 0 : index;
    }

    return active;
  }
}