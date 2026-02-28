import api from '@/lib/api';
import { useState } from 'react';

interface ISortableComponent {
    currentItem: HTMLElement | null;
    _noFinalSort?: boolean;
    placeholder: HTMLElement | null;
}

class SortableComponent implements ISortableComponent {
    public currentItem: HTMLElement | null = null;
    private _storedCSS: Record<string, string> = {};
    private placeholder: HTMLElement | null = null;

    constructor(currentItem: HTMLElement | null) {
        this.currentItem = currentItem;
    }

    revertToLast(): void {
        let delayedTriggers: (() => void)[] = [];
        if (this.reverting) return;

        // Ensure the currentItem parent exists before proceeding
        if (!this._noFinalSort && this.currentItem?.parent()?.length) {
            this.placeholder?.before(this.currentItem);
        }

        this._noFinalSort = null;
        
        if (this.helper[0] === this.currentItem[0]) {  // Assuming helper is a property of the class
            for (const cssProp in this._storedCSS) {
                if (['auto', 'static'].includes(this._storedCSS[cssProp])) {
                    this._storedCSS[cssProp] = '';
                }
            }

            this.currentItem?.css(this._storedCSS).removeClass('ui-sortable-helper');
        } else {
            this.currentItem?.show();
        }
    }

    private get helper(): HTMLElement[] {
        // Placeholder implementation, should be replaced with actual logic
        return [];
    }
}

// Usage example (this would typically be in a React component file)
const sortable = new SortableComponent(document.getElementById('your-element') as HTMLElement);

sortable.revertToLast();