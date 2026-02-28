import React, { Component } from 'react';
import api from '@/lib/api'; // Importing API wrapper instead of raw axios

interface Props {
  content: any; // Replace with actual type if known
  options: any; // Replace with actual type if known
  document: Document;
}

class Tooltip extends Component<Props, {}> {
  liveRegion: HTMLElement;

  constructor(props) {
    super(props);
    this.liveRegion = document.createElement('div');
  }

  componentDidMount() {
    const { content, options } = this.props;

    // Support for screen readers (VoiceOver on macOS, JAWS on IE <=9)
    this.liveRegion.innerHTML = '';
    if (content.clone) {
      let a11yContent = content.clone();
      a11yContent.removeAttribute('id');
      a11yContent.querySelectorAll('[id]').forEach(element => element.removeAttribute('id'));
    } else {
      const a11yContent = content;
    }
    document.body.appendChild(this.liveRegion);
    
    const positionOption = { /* Define your positioning options here */ };
    
    const position = (event: Event) => {
      if (!tooltip.is(":hidden")) {
        tooltip.position(positionOption);
      }
    };

    if (options.track && event && /^mouse/.test(event.type)) {
      this.document.addEventListener('mousemove', position, false);
      // trigger once to override element-relative positioning
      position(event);
    } else {
      const target = options.target || document.body; // Assuming default target is the body
      tooltip.position($.extend({
        of: target,
      }, options.position));
    }

    // Hide the tooltip after setting up the initial position
    tooltip.hide();
  }

  componentWillUnmount() {
    this.document.removeEventListener('mousemove', position, false);
  }

  private _on(document, events) {
    Object.keys(events).forEach(eventName => document.addEventListener(eventName, events[eventName], false));
  }
}

export default Tooltip;