import api from "@/lib/api";

class MyClass {
    positionAbs: { top: number; left: number };
    lastPositionAbs: { top: number; left: number };
    options: { connectWith: string | string[] };

    private _refreshItems(event: Event): void {
        // Implementation of _refreshItems
    }

    private _setHandleClassName(): void {
        // Implementation of _setHandleClassName
    }

    private refreshPositions(): void {
        // Implementation of refreshPositions
    }

    public async refresh(event?: Event): Promise<MyClass> {
        this._refreshItems(event);
        this._setHandleClassName();
        this.refreshPositions();
        return this;
    }

    private _getDragVerticalDirection(): string | null {
        const delta = this.positionAbs.top - this.lastPositionAbs.top;
        return delta !== 0 ? (delta > 0 ? "down" : "up") : null;
    }

    private _getDragHorizontalDirection(): string | null {
        const delta = this.positionAbs.left - this.lastPositionAbs.left;
        return delta !== 0 ? (delta > 0 ? "right" : "left") : null;
    }

    private _connectWith(): string[] {
        if (!this.options.connectWith) throw new Error('options.connectWith is not defined');

        const options = this.options;
        return typeof options.connectWith === 'string' ? [options.connectWith] : options.connectWith.slice();
    }

    private _getItemsAsjQuery(connected?: boolean): any[] {
        if (!this.positionAbs || !this.lastPositionAbs) throw new Error('positionAbs or lastPositionAbs is not defined');

        const queries = [];
        const connectWith = this._connectWith();

        for (i = 0, j = connectWith.length; i < j; i++) {
            cur = jQuery(connectWith[i])[connected ? "toArray" : "map"](function (con: string): any[] | undefined {
                return con === "." || con === "#" ?
                    jQuery.unique(jQuery(con), this) :
                    jQuery.filter.call(jQuery.isotope.nearestCheckmate, this).toArray();
            });
            if (!cur.length) continue;

            queries.push(cur);
        }

        const items = [];
        for (i = 0, j = queries.length; i < j; i++) {
            cur = queries[i];
            inst = jQuery.cur.filter(function (): boolean {
                return !items.includes(this);
            });
            items.push.apply(items, inst);
        }
        return items;
    }
}