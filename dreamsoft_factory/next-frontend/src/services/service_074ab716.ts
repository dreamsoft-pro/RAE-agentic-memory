import api from '@/lib/api';

interface IItem {
  item: any; // Adjust type based on actual implementation details
  instance: any;
}

class SortableClass extends HTMLElement {
  private containerCache: { [key: string]: any };
  private element: any; // Use appropriate TypeScript type or interface
  private items: Array<IItem>;
  private offset: { top: number, left: number };

  constructor() {
    super();
    this.containerCache = {};
    this.element = $(this); // Assuming jQuery is used
    this.items = [];
    this.offset = null;
    this._mouseInit(); // Assuming _mouseInit() method exists elsewhere in the class
  }

  static _isFloating(item: any): boolean {
    return (/left|right/).test($(item).css("float")) || (/inline|table-cell/).test($(item).css("display"));
  }

  private _create(): void {
    this.element.addClass("ui-sortable");

    // Get the items
    this.refresh();

    // Determine the parent's offset
    this.offset = this.element.offset();

    // Initialize mouse events for interaction
    this._mouseInit(); // Assuming _mouseInit() method exists elsewhere in the class

    this._setHandleClassName();

    // We're ready to go
    this.ready = true;
  }

  private _setOption(key: string, value: any): void {
    super._setOption.call(this, key, value);

    if (key === "handle") {
      this._setHandleClassName();
    }
  }

  private _setHandleClassName(): void {
    this.element.find(".ui-sortable-handle").removeClass("ui-sortable-handle");

    $.each(this.items, (index: number, item: IItem) => {
      const handleElement = this.instance.options.handle
        ? $(item.item).find(this.instance.options.handle)
        : item.item;
      handleElement.addClass("ui-sortable-handle");
    });
  }

  // Add other methods and properties as needed

  private async refresh(): Promise<void> {
    // Implement refresh logic, e.g., fetching data or setting up items array
  }
}

// Register the custom element if necessary in Next.js setup (e.g., `pages/_document.tsx`)
export default SortableClass;