import api from "@/lib/api";

class ExampleComponent {
    private cssPosition: string;
    private scrollParent: HTMLElement;
    private document: Document; // Assuming this represents a reference to the current document
    private offsetParent: HTMLElement;

    constructor(cssPosition: string, scrollParent: HTMLElement, document: Document, offsetParent: HTMLElement) {
        this.cssPosition = cssPosition;
        this.scrollParent = scrollParent;
        this.document = document;
        this.offsetParent = offsetParent;
    }

    calculateOffset(po: { left: number; top: number }): void {
        if (this.cssPosition === "absolute" && this.scrollParent !== this.document && this.scrollParent.contains(this.offsetParent)) {
            po.left += this.scrollParent.scrollLeft;
            po.top += this.scrollParent.scrollTop;
        }
    }

    // Other class methods would go here
}