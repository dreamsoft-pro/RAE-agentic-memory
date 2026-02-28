import api from "@/lib/api";

interface WidgetOptions {
  handle?: string;
}

class ItemWidget {
  private currentItem: HTMLElement | null = null;
  private options: WidgetOptions = {};
  private widgetName: string;

  constructor(widgetName: string, options?: Partial<WidgetOptions>) {
    this.widgetName = widgetName;
    if (options) {
      this.options.handle = options.handle || '';
    }
  }

  async _mouseCapture(event: MouseEvent): Promise<boolean> {
    let currentItem: HTMLElement | null = null;

    // Find the clicked item or its parent
    const targetsToCheck = [event.target as HTMLElement, ...document.querySelectorAll(`[data-${this.widgetName}-item="${this.widgetName}"]`)];
    for (const target of targetsToCheck) {
      if (target.closest(`[${this.widgetName}-item="${this.widgetName}"]`) === target) {
        currentItem = target;
        break;
      }
    }

    if (!currentItem) return false;

    let validHandle = this.options.handle ? !!(event.target as HTMLElement).closest(this.options.handle) : true;

    if (!validHandle) return false;

    this.currentItem = currentItem;
    await this._removeCurrentsFromItems();
    return true;
  }

  private async _removeCurrentsFromItems(): Promise<void> {
    // Implementation of the function to remove current items
    console.log('Removing currents from items');
  }

  public async _mouseStart(event: MouseEvent, overrideHandle?: boolean): Promise<void> {
    const o = this.options;

    this.currentContainer = this;
    await this.refreshPositions();
  }

  private refreshPositions(): void {
    // Implementation of the function to refresh positions
    console.log('Refreshing positions');
  }
}

export default ItemWidget;