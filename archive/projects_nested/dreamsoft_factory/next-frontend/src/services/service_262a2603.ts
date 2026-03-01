import React, { Component } from 'react';
import api from '@/lib/api';

class SelectableComponent extends Component {
  private element: HTMLElement | null;
  private dragStarted: boolean;
  private selectees: NodeListOf<HTMLElement>;
  private callbacks = {
    selected: null,
    selecting: null,
    start: null,
    stop: null,
    unselected: null,
    unselecting: null
  };

  componentDidMount() {
    this.element?.classList.add("ui-selectable");
    this.refresh();
    this._mouseInit();
  }

  private refresh = () => {
    if (!this.element) return;

    const selectees = this.element.querySelectorAll<HTMLElement>(this.props.filter);
    
    selectees.forEach((el: HTMLElement) => {
      el.classList.add("ui-selectee");

      const pos = el.getBoundingClientRect();

      api.post("/data", {
        element: el,
        $element: el,
        left: pos.left,
        top: pos.top,
        right: pos.left + el.offsetWidth,
        bottom: pos.top + el.offsetHeight,
        startselected: false,
        selected: el.classList.contains("ui-selected"),
        selecting: el.classList.contains("ui-selecting"),
        unselecting: el.classList.contains("ui-unselecting")
      });
    });

    this.selectees = selectees;
  };

  private _mouseInit() {
    // Implement mouse initialization logic here
  }

  render() {
    return <div ref={el => this.element = el} />;
  }
}

export default SelectableComponent;