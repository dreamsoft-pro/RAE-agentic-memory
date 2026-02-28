import { CanvasRenderingContext2D } from 'canvas';
import api from '@/lib/api'; // Ensure this import is correctly set up in your project

class WorkspaceDrawer {
    private ctx: CanvasRenderingContext2D;
    private workspaceWidth: number;
    private workspaceHeight: number;
    private scale: number;

    constructor(ctx: CanvasRenderingContext2D, width: number, height: number, scale: number) {
        this.ctx = ctx;
        this.workspaceWidth = width;
        this.workspaceHeight = height;
        this.scale = scale;
    }

    public async drawBackground(): Promise<void> {
        this.ctx.translate(0.5, 0.5);
        this.ctx.fillStyle = '#ffffff';
        this.ctx.strokeStyle = '#c8c8c8';
        this.ctx.lineWidth = 1;
        this.ctx.miterLimit = 'round'; // This should be a number, e.g., ctx.miterLimit = 4;
        this.ctx.lineJoin = 'round' as CanvasLineJoin; // Ensure this is set up correctly or use the default value.
        this.ctx.globalAlpha = 1;
        this.ctx.fillRect(0, 0, this.workspaceWidth * this.scale, this.workspaceHeight * this.scale);
    }

    public putLabel(text: string, x: number, y: number, rotation?: number, color: string = '#000000'): void {
        const parsedX = parseInt(`${x}`);
        const parsedY = parseInt(`${y}`);

        this.ctx.save();
        this.ctx.fillStyle = color;
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';

        if (rotation !== undefined) {
            this.ctx.translate(parsedX, parsedY);
            this.ctx.rotate(rotation);
            this.ctx.fillText(text, 0, 0);
        } else {
            this.ctx.fillText(text, parsedX, parsedY);
        }

        this.ctx.restore();
    }
}

// Example usage:
const ctx = c.getContext("2d", { alpha: true }) as CanvasRenderingContext2D;
const drawer = new WorkspaceDrawer(ctx, workspace.width, workspace.height, scale);

drawer.drawBackground().then(() => {
    // Drawing labels after background is drawn
    drawer.putLabel('Example', 50, 50);
});