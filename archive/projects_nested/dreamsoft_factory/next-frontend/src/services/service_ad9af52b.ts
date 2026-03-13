import api from '@/lib/api';
import { useEffect, useState } from 'react';

class SortableComponent extends React.Component<{}, ISortableOptions> {
  static version = "1.11.4";
  static widgetEventPrefix = "sort";

  constructor(props: {}) {
    super(props);
    this.state = {
      appendTo: "parent",
      axis: false,
      connectWith: false,
      containment: false,
      cursor: "auto",
      cursorAt: false,
      dropOnEmpty: true,
      forcePlaceholderSize: false,
      forceHelperSize: false,
      grid: false,
      handle: false,
      helper: "original",
      items: "> *",
      opacity: false,
      placeholder: false,
      revert: false,
      scroll: true,
      scrollSensitivity: 20,
      scrollSpeed: 20,
      scope: "default",
      tolerance: "intersect",
      zIndex: 1000,

      // callbacks
      activate: null as ((event: Event) => void) | null,
      beforeStop: null as ((event: Event) => void) | null,
      change: null as (() => void) | null,
      deactivate: null as ((event: Event) => void) | null,
      out: null as ((event: Event) => void) | null,
      over: null as ((event: Event) => void) | null,
      receive: null as ((event: Event) => void) | null,
      remove: null as ((event: Event) => void) | null,
      sort: null as ((event: Event) => void) | null,
      start: null as ((event: Event) => void) | null,
      stop: null as ((event: Event) => void) | null,
      update: null as ((event: Event) => void) | null
    };
  }

  _isOverAxis(x: number, reference: number, size: number): boolean {
    return (x >= reference) && (x < (reference + size));
  }

  componentDidMount() {
    // Initialization logic for sortable component would go here.
    // For now, it's just an example and doesn't interact with DOM directly.
  }

  render() {
    return (
      <div className="sortable">
        {/* Render items based on this.state.items */}
        {this.state.items.map((item) => (
          <div key={item} style={{ opacity: this.state.opacity ? this.state.opacity : '' }}>
            {item}
          </div>
        ))}
      </div>
    );
  }
}

interface ISortableOptions {
  appendTo?: string;
  axis?: boolean | 'x' | 'y';
  connectWith?: false | string | string[];
  containment?: boolean | HTMLElement | string | (number | number)[];
  cursor?: string;
  cursorAt?: { [key: string]: any };
  dropOnEmpty?: boolean;
  forcePlaceholderSize?: boolean;
  forceHelperSize?: boolean;
  grid?: boolean | [number, number] | ((element: Element) => [number, number]);
  handle?: false | HTMLElement | string;
  helper?: 'clone' | 'original';
  items?: string;
  opacity?: number | null;
  placeholder?: boolean | string;
  revert?: boolean | number | (() => void);
  scroll?: boolean;
  scrollSensitivity?: number;
  scrollSpeed?: number;
  scope?: string;
  tolerance?: 'intersect' | 'fit';

  // callbacks
  activate?: (event: Event) => void;
  beforeStop?: (event: Event) => void;
  change?: () => void;
  deactivate?: (event: Event) => void;
  out?: (event: Event) => void;
  over?: (event: Event) => void;
  receive?: (event: Event) => void;
  remove?: (event: Event) => void;
  sort?: (event: Event) => void;
  start?: (event: Event) => void;
  stop?: (event: Event) => void;
  update?: (event: Event) => void;
}

export default SortableComponent;