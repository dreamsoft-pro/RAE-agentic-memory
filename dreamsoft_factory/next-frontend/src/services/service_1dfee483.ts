import api from "@/lib/api";

class MenuComponent {
    private options: { disabled: boolean };
    private menuItems?: HTMLElement[];
    private isOpen: boolean = false;

    constructor(private button: HTMLElement, private menu: HTMLElement) {}

    private _refreshMenu(): void {
        // Placeholder for refreshing menu items logic
        this.menuItems = document.querySelectorAll('.menu-item'); // Example selector
    }

    private _getSelectedItem(): HTMLElement | null {
        return this.menu.querySelector('.ui-state-focus') || null;
    }

    private _toggleAttr(): void {
        if (this.isOpen) {
            this.button.setAttribute('aria-expanded', 'true');
        } else {
            this.button.removeAttribute('aria-expanded');
        }
    }

    private _resizeMenu(): void {
        // Placeholder for resizing menu logic
    }

    private _position(): void {
        const positionOptions = { of: this.button, my: "left top", at: "left bottom" };
        this.menu.style.position = 'absolute';
        const rectButton = this.button.getBoundingClientRect();
        const rectMenu = this.menu.getBoundingClientRect();

        // Simple positioning example
        this.menu.style.left = `${rectButton.right - rectMenu.width}px`;
        this.menu.style.top = `${rectButton.bottom}px`;
    }

    private _documentClick(event: MouseEvent): void {
        if (!this.menu.contains(event.target as Node)) {
            this.close();
        }
    }

    public open(event?: Event): void {
        if (this.options.disabled) {
            return;
        }

        // If this is the first time the menu is being opened, render the items
        if (!this.menuItems) {
            this._refreshMenu();
        } else {
            const selectedElement = this.menu.querySelector('.ui-state-focus');
            if (selectedElement) {
                selectedElement.classList.remove('ui-state-focus');
            }
            this.menuInstance?.focus(null, this._getSelectedItem());
        }

        this.isOpen = true;
        this._toggleAttr();
        this._resizeMenu();
        this._position();

        document.addEventListener("click", this._documentClick);

        this._trigger("open", event);
    }

    public close(event?: Event): void {
        if (!this.isOpen) {
            return;
        }

        this.isOpen = false;
        this._toggleAttr();

        this.range = null;
        document.removeEventListener("click", this._documentClick);

        this._trigger("close", event);
    }

    public widget(): HTMLElement {
        return this.button;
    }
}