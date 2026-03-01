import api from "@/lib/api";
import $ from 'jquery'; // Assuming jQuery is being used

class Draggable {
    options: any;
    helper: Node[];
    offset: { relative: { left: number; top: number }; parent: { left: number; top: number } };
    containment: [number, number, number, number];
    documentWidth: () => number;
    windowHeight: () => number | number;
    helperProportions: { width: number; height: number };
    margins: { left: number; top: number };

    constructor() {
        this.documentWidth = () => $(document).width();
        this.windowHeight = () => $(window).height() || $(document)[0].body.parentNode.scrollHeight;
    }

    private calculateContainment(): void {
        const o = this.options;

        if (o.containment === "parent") {
            o.containment = this.helper[0].parentNode;
        }

        if (o.containment === "document" || o.containment === "window") {
            this.containment = [
                0 - this.offset.relative.left - this.offset.parent.left,
                0 - this.offset.relative.top - this.offset.parent.top,
                o.containment === "document" ? this.documentWidth() : $(window).width() - this.helperProportions.width - this.margins.left,
                (o.containment === "document" ? this.windowHeight() : $(window).height()) - this.helperProportions.height - this.margins.top
            ];
        }

        if (!(/^(document|window|parent)$/).test(o.containment)) {
            const ce = $(o.containment)[0];
            const co = $(o.containment).offset();
            const over = ($(ce).css("overflow") !== "hidden");
        }
    }
}