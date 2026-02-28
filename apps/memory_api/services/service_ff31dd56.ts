import api from "@/lib/api";

class TabNavigation {
    private active: HTMLElement;
    private tabs: HTMLElement[];
    private options: { active: number; disabled: number[] };

    constructor(active?: HTMLElement, tabs?: HTMLElement[], options?: { active: number; disabled: number[] }) {
        this.active = active || document.querySelector('.active-tab') as HTMLElement;
        this.tabs = tabs || Array.from(document.querySelectorAll('.tab'));
        this.options = options || { active: 0, disabled: [] };
    }

    private _activate(index: number) {
        // Activation logic
        console.log(`Activating tab at index ${index}`);
    }

    private _focusNextTab(index: number, goingForward: boolean): number {
        const lastTabIndex = this.tabs.length - 1;

        function constrain() {
            if (index > lastTabIndex) {
                return 0;
            }
            if (index < 0) {
                return lastTabIndex;
            }
            return index;
        }

        while (this.options.disabled.includes(constrain())) {
            index = goingForward ? index + 1 : index - 1;
        }

        return constrain();
    }

    public handleCtrlUp(event: KeyboardEvent): void {
        if (event.ctrlKey && event.keyCode === 38) { // $.ui.keyCode.UP is typically 38
            event.preventDefault();
            this.active.focus();
        }
    }

    public handlePageNav(event: KeyboardEvent): boolean | undefined {
        if (event.altKey && event.keyCode === 33) { // $.ui.keyCode.PAGE_UP is typically 33
            this._activate(this._focusNextTab(this.options.active - 1, false));
            return true;
        }
        if (event.altKey && event.keyCode === 34) { // $.ui.keyCode.PAGE_DOWN is typically 34
            this._activate(this._focusNextTab(this.options.active + 1, true));
            return true;
        }
    }

    public findNextTab(index: number, goingForward: boolean): number {
        const lastTabIndex = this.tabs.length - 1;

        function constrain() {
            if (index > lastTabIndex) {
                index = 0;
            }
            if (index < 0) {
                index = lastTabIndex;
            }
            return index;
        }

        while (this.options.disabled.includes(constrain())) {
            index = goingForward ? index + 1 : index - 1;
        }

        return constrain();
    }
}

// Example usage
const tabNavInstance = new TabNavigation();
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey || event.altKey) {
        tabNavInstance.handleCtrlUp(event);
        const resultPageNav = tabNavInstance.handlePageNav(event);
        if (resultPageNav === true) { // This will return true if page navigation happened
            console.log('Page navigation occurred');
        }
    }
});