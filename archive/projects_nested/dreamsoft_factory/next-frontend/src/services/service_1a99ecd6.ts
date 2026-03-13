import api from "@/lib/api";
import { useEffect } from "react";

class DragManager {
    containers: any[];
    delayedTriggers: Function[] = [];
    storedCursor: string | null;
    document: any; // Assuming a DOM-like API for simplicity
    helper: any;   // Assuming an element object with css method
    _storedOpacity: number | undefined;
    _storedZIndex: string;

    constructor(containers: any[], document: any, helper: any) {
        this.containers = containers;
        this.document = document;
        this.helper = helper;
    }

    async delayEvent(type: string, instance: any, container: any): Promise<Function> {
        return function(event: any) {
            container._trigger(type, event, instance._uiHash(instance));
        };
    }

    handleDeactivation(noPropagation: boolean): void {
        for (let i = this.containers.length - 1; i >= 0; i--) {
            if (!noPropagation) {
                this.delayedTriggers.push(this.delayEvent("deactivate", this, this.containers[i]));
            }
            if (this.containers[i].containerCache.over) {
                this.delayedTriggers.push(this.delayEvent("out", this, this.containers[i]));
                this.containers[i].containerCache.over = 0;
            }
        }

        // Reset stored properties
        if (this.storedCursor) {
            this.document.find("body").css("cursor", this.storedCursor);
            this.storedStylesheet?.remove();
        }

        if (this._storedOpacity !== undefined) {
            this.helper.css("opacity", this._storedOpacity);
        }

        if (this._storedZIndex) {
            this.helper.css("zIndex", this._storedZIndex === "auto" ? "" : this._storedZIndex);
        }
        
        // Mark dragging state as false
        this.dragging = false;
    }
}