import api from "@/lib/api";
import $ from "jquery"; // Assuming you're using jQuery for DOM manipulation

class TabManager {
    private selectedIndex: number = 0; // Default selected index
    private activating: NodeJS.Timeout | null = null;
    private delay: number = 250; // Example delay value, should be defined in your actual implementation
    public tabs: JQuery;

    constructor(tabs: JQuery) {
        this.tabs = tabs;
    }

    private _focusNextTab(selectedIndex: number, goingForward: boolean): number {
        const tabsCount = this.tabs.length;
        let nextIndex = selectedIndex + (goingForward ? 1 : -1);

        if (nextIndex < 0 || nextIndex >= tabsCount) {
            nextIndex = (nextIndex + tabsCount) % tabsCount;
        }

        return nextIndex;
    }

    private _delay(fn: () => void, delay: number): NodeJS.Timeout {
        return setTimeout(() => fn(), delay);
    }

    public handleTabKeydown(event: KeyboardEvent): void {
        event.preventDefault();
        clearTimeout(this.activating);

        const goingForward = event.keyCode === 39 || event.keyCode === 40; // Right or Down Arrow
        this.selectedIndex = this._focusNextTab(this.selectedIndex, goingForward);

        if (!event.ctrlKey && !event.metaKey) {
            const focusedTab = this.tabs.eq(this.selectedIndex);
            this.tabs.attr("aria-selected", "false");
            focusedTab.attr("aria-selected", "true");

            this.activating = this._delay(() => this.option("active", this.selectedIndex), this.delay);
        }
    }

    private option(key: string, value: any): void {
        // Implement your logic to set options here
    }

    public handlePanelKeydown(event: KeyboardEvent): void | boolean {
        if (this._handlePageNav(event)) return;
        // Add your panel key handling logic here
    }

    private _handlePageNav(event: KeyboardEvent): boolean {
        // Your page navigation handling logic here, return true if handled
        return false;
    }
}

export default TabManager;