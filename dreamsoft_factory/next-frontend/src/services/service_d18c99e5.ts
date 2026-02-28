import $ from 'jquery';
import '@/lib/api'; // Assuming api import is not needed for this conversion

class Tabs {
    private panels: JQuery;
    private tabs: JQuery;
    private anchors: JQuery;
    private tablist?: JQuery;

    constructor() {
        this.panels = $('#panels'); // Replace with actual initialization
        this.tabs = $('#tabs');     // Replace with actual initialization
        this.anchors = $('.anchors'); // Replace with actual initialization
    }

    public initializePanels(): void {
        this.panels
            .addClass( "ui-tabs-panel ui-widget-content ui-corner-bottom" )
            .attr( "role", "tabpanel" );

        const prevTabs: JQuery | undefined = /* Define or retrieve prevTabs */;
        if (prevTabs) {
            this._off(prevTabs.not(this.tabs));
            // Assuming _off and not methods are defined elsewhere
            this._off(prevTabs.not(this.anchors)); // anchors should be initialized before usage
            this._off(prevTabs.not(this.panels));  // panels should be initialized before usage
        }
    }

    private _getList(): JQuery {
        return this.tablist || this.element.find( "ol,ul" ).eq(0);
    }

    private _createPanel(id: string): JQuery {
        return $("<div>")
            .attr("id", id)
            .addClass("ui-tabs-panel ui-widget-content ui-corner-bottom")
            .data("ui-tabs-destroy", true);
    }

    private _setupDisabled(disabled: any[]): boolean | false {
        if ($.isArray(disabled)) {
            if (!disabled.length) {
                return false;
            } else if (disabled.length === this.anchors.length) {
                return true;
            }
        }
        return disabled; // Return original value if not an array
    }

    private _off(elements: JQuery): void {
        elements.off(); // Assuming off method is defined elsewhere
    }

    private element: JQuery = $('#element'); // Replace with actual initialization for this.element

    public setTablist(list: JQuery | undefined) {
        this.tablist = list;
    }
}

export default Tabs;