import React, { Component } from 'react';
import axios from '@/lib/api'; // Assuming this is the custom Axios instance setup

interface ScrollOptions {
  scrollSensitivity: number;
  scrollSpeed: number;
}

export default class MyScrollComponent extends Component<{ [key: string]: any }, {}> {
  
  overflowOffset = { top: 0, left: 0 };
  scrollParent: HTMLDivElement | null = null;

  // Assuming you have access to the event and `scrollOptions` in your method
  handleScrollEvent = async (event: MouseEvent, scrollOptions: ScrollOptions) => {

    const scrolled = this.calculateScrollPosition(event, scrollOptions);

    if (!this.scrollParent || !scrolled) return;
    
    this.scrollParent.scrollTop = scrolled.top;
    this.scrollParent.scrollLeft = scrolled.left;

  }

  calculateScrollPosition = (event: MouseEvent, options: ScrollOptions): { top?: number; left?: number } => {
    let scrollTop: number | undefined;
    let scrollLeft: number | undefined;

    if ((this.overflowOffset.top + this.scrollParent!.offsetHeight) - event.pageY < options.scrollSensitivity) {
      scrollTop = this.scrollParent!.scrollTop + options.scrollSpeed;
    } else if (event.pageY - this.overflowOffset.top < options.scrollSensitivity) {
      scrollTop = this.scrollParent!.scrollTop - options.scrollSpeed;
    }

    if ((this.overflowOffset.left + this.scrollParent!.offsetWidth) - event.pageX < options.scrollSensitivity) {
      scrollLeft = this.scrollParent!.scrollLeft + options.scrollSpeed;
    } else if (event.pageX - this.overflowOffset.left < options.scrollSensitivity) {
      scrollLeft = this.scrollParent!.scrollLeft - options.scrollSpeed;
    }

    return { top: scrollTop, left: scrollLeft };
  }
}