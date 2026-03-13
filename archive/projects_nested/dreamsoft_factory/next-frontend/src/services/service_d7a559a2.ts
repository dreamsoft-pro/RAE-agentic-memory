import api from "@/lib/api";
import $ from "jquery";

class TooltipComponent {
    private tooltips: Record<string, { element: JQuery; tooltip: JQuery }> = {};
    
    public _tooltip(element: JQuery): void {
        let tooltip = $("<div>")
            .attr("role", "tooltip")
            .addClass(`ui-tooltip ui-widget ui-corner-all ui-widget-content ${this.options.tooltipClass || ""}`);
        
        const id = tooltip.uniqueId().attr("id");

        $("<div>").addClass("ui-tooltip-content").appendTo(tooltip);

        tooltip.appendTo(this.document[0].body);
        
        this.tooltips[id] = { element, tooltip };
    }

    public _find(target: JQuery): Record<string, { element: JQuery; tooltip: JQuery }> | null {
        const id = target.data("ui-tooltip-id");
        return id ? this.tooltips[id] : null;
    }

    public async _removeTooltip(tooltip: JQuery) {
        tooltip.remove();
        delete this.tooltips[tooltip.attr("id")];
    }

    public _destroy() {
        for (const key in this.tooltips) {
            if (Object.prototype.hasOwnProperty.call(this.tooltips, key)) {
                const tooltip = this.tooltips[key].tooltip;
                $(document).off(`mouseleave focusout`, `${key}.remove`).off(`mouseenter focus`.concat(".open", ` ${key}`));
                this._removeTooltip(tooltip);
            }
        }

        // Reset all options to their default values
        for (const option in this.options) {
            if (Object.prototype.hasOwnProperty.call(this.options, option)) {
                this.setOption(option as keyof typeof this.options, this._defaults[option]);
            }
        }
    }

    private _defaults = {
        tooltipClass: "",
        // Define any other default options here
    };

    private setOption(key: string, value: unknown): void {
        if (this._setOptions) {  // Assuming there's a method to handle setting options
            this._setOptions({ [key]: value });
        } else {
            this.options[key] = value;
        }
    }

    private _setOptions: ((options: Record<string, unknown>) => void) | undefined;

    constructor(private document: { [0]: Document }, private options: Record<string, unknown>, private _setOptions?: (options: Record<string, unknown>) => void) {
    }
}