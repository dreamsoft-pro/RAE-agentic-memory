import api from '@/lib/api';
import $ from 'jquery'; // Assuming jQuery is used as an external library

class SelectableComponent {
    private helper: JQuery;
    private selectees: JQuery;

    constructor(private element: HTMLElement) {}

    public init(): void {
        this.helper = $("<div class='ui-selectable-helper'></div>");
    }

    private _destroy(): void {
        if (!this.selectees || !this.element) return;

        this.selectees
            .removeClass("ui-selectee")
            .removeData("selectable-item");

        this.element
            .removeClass("ui-selectable ui-selectable-disabled");
        
        // Assuming there is a method `_mouseDestroy` in the class or imported from somewhere
        this._mouseDestroy();
    }

    private async _mouseStart(event: MouseEvent): Promise<void> {
        const that = this;
        const options = this.options;

        if (!options) return;

        this.opos = [event.pageX, event.pageY];

        if (options.disabled) {
            return;
        }

        this.selectees = $(options.filter, this.element);

        await this._trigger("start", event); // Assuming _trigger returns a promise or is async

        const appendTo: JQuery = options.appendTo; // Assuming `options.appendTo` is a jQuery object
        if (!appendTo) return;

        appendTo.append(this.helper);
        
        this.helper.css({
            "left": event.pageX,
            "top": event.pageY,
            "width": 0,
            "height": 0
        });

        if (options.autoRefresh) {
            await this.refresh(); // Assuming `refresh` returns a promise or is async
        }
    }

    private _mouseDestroy(): void {}

    private options: { disabled?: boolean, filter?: string, appendTo?: JQuery } = {}; // Example of how options might be defined

    public refresh(): Promise<void> {
        return new Promise((resolve) => {
            setTimeout(() => resolve(), 100); // Mock implementation
        });
    }

    private _trigger<T extends keyof SelectableComponent['options']>(event: T, data?: any): Promise<void> {
        return new Promise(resolve => {
            // Implementation of event triggering logic
            resolve();
        });
    }
}

export default SelectableComponent;