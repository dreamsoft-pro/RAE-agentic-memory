import api from "@/lib/api";
import { useRef, useEffect } from "react";

class DraggableComponent extends React.Component {
    private document: Document;
    private offsetParent: HTMLElement | null = null; // Placeholder for the actual DOM element reference.
    private currentItem: any; // Replace this with proper typing or a specific component if known.
    private helper: any; // Replace this with proper typing or a specific component if known.
    private scrollParent: HTMLElement | null = null; // Placeholder for the actual DOM element reference.

    componentDidMount() {
        this.document = document;
        this.offsetParent = this.getDocumentElement();
        this.scrollParent = this.getScrollParent(this.currentItem);
    }

    _getBoundingClientRectWithOffsetParentFix(): { top: number, left: number } | undefined {
        let po: { top?: number; left?: number } = {};

        if (!this.offsetParent) return;

        // This condition checks for specific IE edge cases.
        if (this.offsetParent === this.document.body || (this.offsetParent.tagName && this.offsetParent.tagName.toLowerCase() === "html")) {
            po = { top: 0, left: 0 };
        }

        const borderTopWidth = parseInt(window.getComputedStyle(this.offsetParent).borderTopWidth);
        const borderLeftWidth = parseInt(window.getComputedStyle(this.offsetParent).borderLeftWidth);

        return {
            top: po.top + (Number.isNaN(borderTopWidth) ? 0 : borderTopWidth),
            left: po.left + (Number.isNaN(borderLeftWidth) ? 0 : borderLeftWidth)
        };
    }

    private getDocumentElement() {
        let element = this.document.body;
        if (!element || element.nodeType !== Node.ELEMENT_NODE) return null;

        const rootEl = this.document.documentElement as HTMLElement | undefined;

        // Check if the body has been injected into the DOM
        const isHtmlShadowRootBody = this.document.body instanceof ShadowRoot;
        const isRootShadowRoot = this.document.getRootNode() === this.document && (rootEl?.shadowRoot !== null);
        
        return (isHtmlShadowRootBody || isRootShadowRoot) ? rootEl : element;
    }

    private getScrollParent(element: HTMLElement): HTMLElement {
        // Implement logic to find the scrollable parent.
        return element.closest('.scrollable-parent') as HTMLElement; // Example selector for a scrollable parent
    }

    _getRelativeOffset(): { top: number, left: number } {
        if (this.currentItem.cssPosition === "relative") {
            const p = this.currentItem.position(); // This needs to be adapted according to React/TypeScript context.
            return {
                top: p.top - (parseInt(this.helper?.style.top || '0', 10)) + this.scrollParent.scrollTop,
                left: p.left - (parseInt(this.helper?.style.left || '0', 10)) + this.scrollParent.scrollLeft
            };
        } else {
            return { top: 0, left: 0 };
        }
    }

    // Any other methods or logic can be similarly adapted as required.
}

export default DraggableComponent;