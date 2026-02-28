import React from 'react';
import api from '@/lib/api'; // Assuming the API module has been correctly set up

class MenuComponent extends React.Component {
    private menuItems: any;
    private element: HTMLSelectElement | null = null;
    private focusIndex: number = 0;
    private isOpen: boolean = false;
    private range?: Range;

    private async _move(direction: string, event: Event): Promise<void> {
        let item: HTMLElement | undefined,
            next: HTMLElement | undefined,
            filter: string = ".ui-menu-item";

        if (this.isOpen) {
            item = this.menuItems.eq(this.focusIndex);
        } else {
            item = this.element ? this.menuItems.eq(this.element[0].selectedIndex) : null;
            filter += ":not(.ui-state-disabled)";
        }

        if (!item || !direction) return;

        if (direction === "first" || direction === "last") {
            next = direction === "first"
                ? item.prevAll(filter).eq(-1)
                : item.nextAll(filter).eq(0);
        } else {
            next = item[direction + "All"](filter).eq(0);
        }

        if (next && next.length) {
            this.menuInstance.focus(event, next);
        }
    }

    private _getSelectedItem(): HTMLElement | null {
        return this.element ? this.menuItems.eq(this.element[0].selectedIndex) : null;
    }

    private _toggle(event: Event): void {
        const action = this.isOpen ? 'close' : 'open';
        if (this[action]) {
            this[action](event);
        }
    }

    private _setSelection(): void {
        let selection;

        if (!this.range) return;

        if (window.getSelection) {
            selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(this.range);
        }
    }
}

export default MenuComponent;