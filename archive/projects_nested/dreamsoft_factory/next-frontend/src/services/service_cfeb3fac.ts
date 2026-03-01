import api from '@/lib/api';

class DraggableElement {
    helperProportions: { width: number; height: number };
    options: { axis: string };
    positionAbs: { top: number; left: number };
    offset: { click: { top: number; left: number } };

    // This method checks if a point is within the helper element's bounds
    private _intersectsWithPointer(item: any): boolean {
        const resource = this.helperProportions;
        const x1 = item.left, y1 = item.top,
              x2 = x1 + item.width, y2 = y1 + item.height,
              t = this.positionAbs.top + this.offset.click.top,
              l = this.positionAbs.left + this.offset.click.left,
              r = l + resource.width,
              b = t + resource.height;

        return (
            (l < x1 + (resource.width / 2) && 
             x2 - (resource.width / 2) < r &&
             t < y1 + (resource.height / 2) &&
             y2 - (resource.height / 2) < b)
        );
    }

    // This method checks if the current position is over an element
    private _intersectsWithPointer(item: any): boolean {
        const options = this.options;
        const axisSpecificStopper = (options.axis === "x") || (options.axis === "y");
        let verticalDirection, horizontalDirection;

        const isOverElementHeight = axisSpecificStopper ||
            this._isOverAxis(this.positionAbs.top + this.offset.click.top, item.top, item.height);

        const isOverElementWidth = axisSpecificStopper ||
            this._isOverAxis(this.positionAbs.left + this.offset.click.left, item.left, item.width);

        if (!isOverElementHeight || !isOverElementWidth) {
            return false;
        }

        verticalDirection = this._getDragVerticalDirection();
        horizontalDirection = this._getDragHorizontalDirection();

        // This is where you would normally check the directions for further logic
        // Since the methods _getDragVerticalDirection and _getDragHorizontalDirection are not defined,
        // we'll assume they return boolean values indicating direction.

        return true;  // Assuming further checks would be done here based on vertical/horizontal direction.
    }

    private async _someAsyncApiCall() {
        try {
            const response = await api.get('/endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('API call failed', error);
        }
    }

    // Placeholder for other methods like _isOverAxis, _getDragVerticalDirection and _getDragHorizontalDirection
}