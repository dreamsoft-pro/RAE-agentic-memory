import api from "@/lib/api";

class DragAndDropHelper {
    private positionAbs: { left: number; top: number };
    private helperProportions: { width: number; height: number };
    private offset: { click: { top: number; left: number } };
    private options: { axis?: string; tolerance?: string; forcePointerForContainers?: boolean; floating?: boolean };

    constructor(positionAbs: { left: number; top: number }, helperProportions: { width: number; height: number }, offset: { click: { top: number; left: number } }, options: { axis?: string; tolerance?: string; forcePointerForContainers?: boolean; floating?: boolean }) {
        this.positionAbs = positionAbs;
        this.helperProportions = helperProportions;
        this.offset = offset;
        this.options = options;
    }

    public checkOverlap(item: { left: number; top: number; width: number; height: number }): boolean {
        const x1 = this.positionAbs.left,
            x2 = x1 + this.helperProportions.width,
            y1 = this.positionAbs.top,
            y2 = y1 + this.helperProportions.height,
            l = item.left,
            r = l + item.width,
            t = item.top,
            b = t + item.height,
            dyClick = this.offset.click.top,
            dxClick = this.offset.click.left;

        const isOverElementHeight = (this.options.axis === "x") || ((y1 + dyClick) > t && (y1 + dyClick) < b),
            isOverElementWidth = (this.options.axis === "y") || ((x1 + dxClick) > l && (x1 + dxClick) < r);

        const isOverElement = isOverElementHeight && isOverElementWidth;

        if (
            this.options.tolerance === "pointer" ||
            this.options.forcePointerForContainers ||
            (this.options.tolerance !== "pointer" && this.helperProportions[this.floating ? "width" : "height"] > item[this.floating ? "width" : "height"])
        ) {
            return isOverElement;
        } else {
            // Add your logic here based on the rest of the code you want to convert
            return false; // Placeholder for further implementation
        }
    }

    public async fetchData(url: string): Promise<void> {
        try {
            const response = await api.get(url);
            console.log(response.data); // Example usage, actual handling should be implemented based on requirements
        } catch (error) {
            console.error("Failed to fetch data:", error);
        }
    }

    private async performSomeOperation(): Promise<void> {
        await this.fetchData("/api/some-endpoint");
    }
}

// Usage example:
const dragAndDropHelper = new DragAndDropHelper(
    { left: 10, top: 20 },
    { width: 100, height: 50 },
    { click: { top: 30, left: 40 } },
    { axis: "x", tolerance: "pointer", forcePointerForContainers: false }
);

dragAndDropHelper.performSomeOperation().then(() => {
    const isOverlapping = dragAndDropHelper.checkOverlap({ left: 50, top: 60, width: 80, height: 40 });
    console.log("Is overlapping:", isOverlapping);
});