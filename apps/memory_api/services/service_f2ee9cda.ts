import React, { Component } from 'react';
import api from '@/lib/api';

interface Props {
  options: any;
}

class ElementEffect extends Component<Props> {
  constructor(props: Props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    const el = document.querySelector(this.props.options.target);
    if (!el) return;

    const o = { ...this.props.options };
    const mode = $.effects.setMode(el, o.mode || "effect");
    let percent: number;
    
    try {
      percent = parseInt(o.percent, 10);
    } catch (e) {
      percent = (mode === "hide") ? 0 : 100;
    }

    if (isNaN(percent)) {
      percent = (mode === "hide" ? 0 : 100);
    }

    const direction = o.direction || "both";
    const origin = o.origin;
    
    const original = {
      height: el.offsetHeight,
      width: el.offsetWidth,
      outerHeight: el.offsetHeight + window.getComputedStyle(el).borderTopWidth.replace('px', '') * 2 +
                   window.getComputedStyle(el).borderBottomWidth.replace('px', '') * 2,
      outerWidth: el.offsetWidth + window.getComputedStyle(el).borderLeftWidth.replace('px', '') * 2 +
                  window.getComputedStyle(el).borderRightWidth.replace('px', '') * 2
    };

    const factor = {
      y: direction !== "horizontal" ? (percent / 100) : 1,
      x: direction !== "vertical" ? (percent / 100) : 1
    };
    
    // We are going to pass this effect to the size effect:
    o.effect = "size";
    o.queue = false;
    o.complete = this.props.options.complete;

    if (mode !== "effect") {
      o.origin = origin || [ "middle", "center" ];
      o.restore = true;
    }
    
    // Proceed with further actions based on the options and state
  }

  render() {
    return <div />;
  }
}

export default ElementEffect;