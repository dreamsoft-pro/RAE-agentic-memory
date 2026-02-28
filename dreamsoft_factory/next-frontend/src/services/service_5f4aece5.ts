import api from "@/lib/api";
import { CanvasRenderingContext2D } from "canvas";

class MyCanvasComponent {
    private workspace: { width: number; height: number };
    private aResult: { longSide: number; shortSide: number; isHorizontalWidth: boolean; isDoubledPages: boolean };
    private formatWidth: number;
    private formatHeight: number;
    private scale: number;
    private ctx: CanvasRenderingContext2D;

    constructor(workspace: { width: number; height: number }, aResult: { longSide: number; shortSide: number; isHorizontalWidth: boolean; isDoubledPages: boolean }, formatWidth: number, formatHeight: number, scale: number, ctx: CanvasRenderingContext2D) {
        this.workspace = workspace;
        this.aResult = aResult;
        this.formatWidth = formatWidth;
        this.formatHeight = formatHeight;
        this.scale = scale;
        this.ctx = ctx;

        this.drawCanvas();
    }

    private async drawCanvas() {
        const x = this.workspace.width >= this.workspace.height ? this.aResult.longSide : this.aResult.shortSide;
        const y = this.workspace.width >= this.workspace.height ? this.aResult.shortSide : this.aResult.longSide;
        const hor = this.aResult.isHorizontalWidth ? this.formatWidth : this.formatHeight;
        const vert = this.aResult.isHorizontalWidth ? this.formatHeight : this.formatWidth;

        for (let i = 0; i < x; i++) {
            for (let j = 0; j < y; j++) {
                this.ctx.rect(hor * i * this.scale, vert * j * this.scale, hor * this.scale, vert * this.scale);
                this.ctx.stroke();
                if(this.aResult.isDoubledPages) {
                    this.ctx.save();
                    this.ctx.beginPath(); // You need to add more code here based on the full requirements of your application.
                    // Assuming you want to continue drawing or adding shapes after save and beginPath
                }
            }
        }
    }

    // Example usage in a Next.js page component (You might use this.drawCanvas() in an event handler or useEffect)
}