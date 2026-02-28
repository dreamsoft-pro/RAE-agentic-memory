import api from "@/lib/api";
import $ from "jquery";

class MyComponent {
  domPosition: { prev?: HTMLElement; parent?: HTMLElement };
  currentItem: HTMLElement;

  constructor() {
    this.domPosition = {};
    this.currentItem = document.createElement("div");
  }

  positionDomElements(): void {
    if (this.domPosition.prev) {
      $(this.domPosition.prev).after(this.currentItem);
    } else {
      $(this.domPosition.parent).prepend(this.currentItem);
    }
  }

  serialize(o?: { connected: boolean }): string {
    const items = this._getItemsAsjQuery(o?.connected);
    const str: string[] = [];
    o = o || {};

    $(items).each((_, item) => {
      const res = ($(o.item || item).attr(o.attribute || "id") || "")
        .match(o.expression || /(.*?)\[(?:=|\+|_)\]([^\[\]]+)/);
      if (res) {
        str.push(
          o.key
            ? `${o.key}=${res[1]}`
            : `${(o.key && o.expression ? res[1] : "")}${res[2]}`
        );
      }
    });

    if (!str.length && o.key) {
      str.push(o.key + "=");
    }

    return str.join("&");
  }

  toArray(o?: { connected: boolean }): string[] {
    const items = this._getItemsAsjQuery(o?.connected);
    const ret: string[] = [];
    o = o || {};

    $(items).each((_, item) => {
      ret.push(
        ($(o.item || item).attr(o.attribute || "id") || "").toString()
      );
    });
    return ret;
  }

  private _getItemsAsjQuery(connected?: boolean): HTMLElement[] {
    // Implementation based on your logic or requirements
    throw new Error("Implement this method");
  }
}

export default MyComponent;