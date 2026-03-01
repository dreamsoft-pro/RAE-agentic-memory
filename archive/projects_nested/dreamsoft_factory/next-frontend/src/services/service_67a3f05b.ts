import api from '@/lib/api';

class SliderComponent {
  private options: any;
  private element: JQuery<HTMLElement>;
  private handles: JQuery<HTMLElement>[] = [];
  
  // Other methods and constructor would be defined here
  
  _refresh(): void {
    this._createRange();
    this._createHandles();
    this._setupEvents();
    this._refreshValue();
  }

  private _createHandles(): void {
    let i, handleCount;
    
    const options = this.options;
    const existingHandles = this.element.find('.ui-slider-handle').addClass('ui-state-default ui-corner-all');
    const handle: string = '<span class="ui-slider-handle ui-state-default ui-corner-all" tabindex="0"></span>';
    const handles: string[] = [];

    if (!options) {
      throw new Error('Options must be defined.');
    }

    handleCount = (options.values && options.values.length) || 1;

    if (existingHandles.length > handleCount) {
      existingHandles.slice(handleCount).remove();
      existingHandles = existingHandles.slice(0, handleCount);
    }

    for (i = existingHandles.length; i < handleCount; i++) {
      handles.push(handle);
    }

    this.handles = existingHandles.add($(handles.join('')).appendTo(this.element));
    
    if (!this.handles || !Array.isArray(this.handles) || this.handles.length === 0) {
      throw new Error('No slider handles found or created.');
    }
    
    this.handle = this.handles.eq(0);
    this.handles.each((index, element) => {
      $(element).data('ui-slider-handle-index', index);
    });
  }

  // Other methods...
}