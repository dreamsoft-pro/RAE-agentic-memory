import api from '@/lib/api';

class TooltipManager {
    private readonly options: { disabled?: boolean } = {};

    constructor(options?: { disabled?: boolean }) {
        if (options) this.options.disabled = options.disabled;
    }

    private _removeDescribedBy(elem: HTMLElement): void {
        const id = elem.dataset.uiTooltipId;
        const describedby = (elem.getAttribute("aria-describedby") || "").split(/\s+/);
        const index = describedby.indexOf(id);

        if (index !== -1) {
            describedby.splice(index, 1);
        }

        elem.removeAttribute("data-ui-tooltip-id");
        const trimmedDescribedBy = $.trim(describedby.join(" "));
        if (trimmedDescribedBy) {
            elem.setAttribute("aria-describedby", trimmedDescribedBy);
        } else {
            elem.removeAttribute("aria-describedby");
        }
    }

    private async _create(): Promise<void> {
        this._removeDescribedByTrigger('mouseover');
        this._removeDescribedByTrigger('focusin');

        // Assuming tooltips and parents are managed as part of the class state
        this.tooltips = {};  // Should be defined somewhere in your class state or initialization
        this.parents = {};   // Similarly, should be a part of your class state

        if (this.options.disabled) {
            await this._disable();
        }
    }

    private _removeDescribedByTrigger(event: string): void {
        // Implement logic for adding event listeners to remove described by on mouseover and focusin
    }

    private async _disable(): Promise<void> {
        // Implementation of disabling the tooltip feature
    }
}