import { useEffect } from 'react';
import axios from '@/lib/api';

export default class Tooltip {
  private elem: HTMLElement;
  private options: TooltipOptions;
  private id: string;

  constructor(elem: HTMLElement) {
    this.elem = elem;
    // Set the defaults for the tooltip plugin
    this.options = {
      content: () => this.getContent(),
      hide: true,
      items: '[title]:not([disabled])',
      position: { my: 'left top', at: 'left bottom', collision: 'flipfit flip' },
      show: true,
      tooltipClass: null,
      track: false,

      close: null as ((event: Event, ui: TooltipUIParams) => void) | null,
      open: null as ((event: Event, ui: TooltipUIParams) => void) | null
    };
  }

  private async getContent(): Promise<string> {
    const title = this.elem.getAttribute('title') || '';
    return `<a>${title}</a>`;
  }

  public initialize() {
    this.id = `ui-tooltip-${Math.random().toString(36).substr(2, 9)}`;
    this.addDescribedBy();
  }

  private addDescribedBy(): void {
    const describedby: string[] = [];
    if (this.elem.getAttribute('aria-describedby')) {
      describedby.push(...this.elem.getAttribute('aria-describedby').split(/\s+/));
    }
    describedby.push(this.id);
    this.elem.setAttribute('aria-describedby', describedby.join(' '));
  }

  public async showTooltip(): Promise<void> {
    const content = await this.getContent();
    // Here you would add logic to show the tooltip, which typically involves React rendering or DOM manipulation.
    console.log(content); // Placeholder for actual implementation
  }
}

interface TooltipOptions {
  content: () => string | Promise<string>;
  hide?: boolean;
  items?: string;
  position?: { my?: string; at?: string; collision?: string };
  show?: boolean;
  tooltipClass?: string;
  track?: boolean;

  close?: (event: Event, ui: TooltipUIParams) => void;
  open?: (event: Event, ui: TooltipUIParams) => void;
}

interface TooltipUIParams {
  element: HTMLElement; // Example property to match the original jQuery UI structure
}