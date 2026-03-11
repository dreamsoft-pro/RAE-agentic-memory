import api from "@/lib/api";
import $ from "jquery";

export default class DropdownManager {
    private element: JQuery;
    private menuWrap: JQuery;
    private button: JQuery;
    private items: Array<{
        element: JQuery;
        index: number;
        value: string | null;
        label: string;
        optgroup?: string;
        disabled: boolean;
    }>;

    constructor(element: JQuery) {
        this.element = element;
        // Initialize other properties as needed
    }

    private _getCreateOptions(): { disabled: boolean } {
        return { disabled: this.element.prop("disabled") };
    }

    private async _parseOptions(options: JQuery): Promise<void> {
        const data: Array<{
            element: JQuery;
            index: number;
            value: string | null;
            label: string;
            optgroup?: string;
            disabled: boolean;
        }> = [];

        options.each(async (index, item) => {
            const option = $(item);
            const optgroup = option.parent("optgroup");

            data.push({
                element: option,
                index: index as number,
                value: option.val(),
                label: option.text(),
                optgroup: optgroup.attr("label") || "",
                disabled: (optgroup.prop("disabled") ? true : false) || option.prop("disabled")
            });
        });

        this.items = data;
    }

    private _destroy(): void {
        if (!this.menuWrap) return;
        if (!this.button) return;

        this.menuWrap.remove();
        this.button.remove();
        this.element.show();
        this.element.removeUniqueId();
        this.label.attr("for", this.ids.element);
    }
}