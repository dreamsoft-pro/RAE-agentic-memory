import api from "@/lib/api";
import $ from "jquery"; // Assuming jQuery is available for DOM manipulation

class DragAndDropHelper {
    private domPosition: { prev?: HTMLElement; parent?: HTMLElement };
    private currentItem: JQuery;
    private helper: JQuery;
    private document: JQueryStatic;
    private storedCursor: string | null = null;
    private storedStylesheet: JQuery | null = null;

    constructor(currentItem: JQuery, helper: JQuery) {
        this.currentItem = currentItem;
        this.helper = helper;
        this.document = $(document);
        this.domPosition = { prev: undefined, parent: undefined };
    }

    public initializeDragDrop(o: any): void {
        // Cache the former DOM position
        if (this.currentItem.prev().length > 0 && this.currentItem.parent().length > 0) {
            this.domPosition.prev = this.currentItem.prev()[0];
            this.domPosition.parent = this.currentItem.parent()[0];
        }

        // If the helper is not the original, hide the original so it's not playing any role during the drag
        if (this.helper[0] !== this.currentItem[0]) {
            this.currentItem.hide();
        }

        // Create the placeholder
        this._createPlaceholder();

        // Set a containment if given in the options
        if (o.containment) {
            this._setContainment();
        }

        if (o.cursor && o.cursor !== "auto") { // cursor option
            const body = this.document.find("body");

            // support: IE
            this.storedCursor = body.css("cursor");
            body.css("cursor", o.cursor);

            this.storedStylesheet = $("<style>*{ cursor: " + o.cursor + " !important; }</style>").appendTo(body);
        }

        if (o.opacity) { // opacity option
            if (this.helper.css("opacity")) {
                this._storedOpacity = this.helper.css("opacity");
            }
            this.helper.css("opacity", o.opacity);
        }
    }

    private _createPlaceholder(): void {
        // Placeholder creation logic here
    }

    private _setContainment(): void {
        // Containment setting logic here
    }

    private _storedOpacity: string | null = null;
}