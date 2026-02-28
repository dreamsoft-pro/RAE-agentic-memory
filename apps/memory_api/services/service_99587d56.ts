import api from '@/lib/api';

class SortableComponent {
    private offset: any;
    private margins: any;
    private offsetParent: any;
    private document: any;
    private helper: HTMLElement;
    private dragging: boolean;
    private currentItem: HTMLElement;
    private storedCSS: any;
    private options: { revert?: string };

    public animateOrClear(event: Event, noPropagation: boolean): void {
        const cur = this.getHelperPosition(); // Assume getHelperPosition() returns the position object
        let animation = {};

        if (!this.options.axis || this.options.axis === "x") {
            animation.left = cur.left - this.offset.parent.left - this.margins.left + (this.offsetParent[0] === this.document[0].body ? 0 : this.offsetParent[0].scrollLeft);
        }
        if (!this.options.axis || this.options.axis === "y") {
            animation.top = cur.top - this.offset.parent.top - this.margins.top + (this.offsetParent[0] === this.document[0].body ? 0 : this.offsetParent[0].scrollTop);
        }

        this.reverting = true;
        
        // Assuming `$(this.helper).animate` is a jQuery method
        $(this.helper).animate(animation, parseInt(this.options.revert || "500", 10), async () => {
            await this._clear(event as MouseEvent); // Assuming _clear returns a Promise
        });
    }

    public cancel(): void {
        if (this.dragging) {
            this._mouseUp({ target: null });

            if (this.options.helper === "original") {
                $(this.currentItem).css(this.storedCSS).removeClass("ui-sortable-helper");
            } else {
                $(this.currentItem).show();
            }
        }
    }

    private _clear(event?: MouseEvent): Promise<void> {
        // Placeholder for the actual implementation
        return new Promise((resolve) => resolve());
    }

    private _mouseUp(event: { target: Element }): void {
        // Placeholder for the actual implementation
    }

    constructor() {
        this.offset = {};
        this.margins = {};
        this.offsetParent = [];
        this.document = [document];
        this.helper = document.createElement('div');
        this.dragging = false;
        this.currentItem = document.createElement('div');
        this.storedCSS = {};
        this.options = { revert: "500" }; // Default options
    }
}