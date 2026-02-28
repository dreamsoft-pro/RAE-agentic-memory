import api from "@/lib/api";
import { DragEvent } from "react";

class SortableHelper {
    private helper: HTMLElement;
    private options: any; // Replace 'any' with actual type definition based on your application.
    private scrollParent: HTMLElement;
    private document: Document;

    constructor(helper: HTMLElement, options: any, scrollParent: HTMLElement, doc: Document) {
        this.helper = helper;
        this.options = options;
        this.scrollParent = scrollParent;
        this.document = doc;
    }

    public addClass(className: string): void {
        this.helper.classList.add(className);
    }

    private _generatePosition(event: DragEvent): { top: number; left: number } {
        // Implementation of generate position logic
        return { top: event.clientY, left: event.clientX };
    }

    private _convertPositionTo(relative: "absolute"): { top: number; left: number } {
        // Implementation of convert position to absolute logic
        return this._generatePosition({ clientX: 0, clientY: 0 });
    }

    public async _mouseDrag(event: DragEvent): Promise<void> {
        const o = this.options;
        let scrolled = false;

        // Compute the helpers position
        const position = this._generatePosition(event);
        const positionAbs = this._convertPositionTo("absolute");

        if (!this.lastPositionAbs) {
            this.lastPositionAbs = positionAbs;
        }

        // Do scrolling
        if (o.scroll) {
            if (this.scrollParent[0] !== this.document[0] && this.scrollParent[0].tagName !== "HTML") {
                // Scrolling logic implementation here.
            }
        }

        // Additional drag logic can be added here.

        return;
    }

    public handleStartDrag(event: DragEvent): boolean | void {
        this.helper.classList.add("ui-sortable-helper");
        this._mouseDrag(event); // Execute the drag once - this causes the helper not to be visible before getting its correct position
        return true;
    }
}