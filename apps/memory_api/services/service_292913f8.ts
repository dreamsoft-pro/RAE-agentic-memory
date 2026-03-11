import api from '@/lib/api';
import { useEffect } from 'react';

interface IEffectProps {
  mode?: string;
  direction?: string;
  distance?: number;
  times?: number;
  duration?: number;
}

class EffectComponent extends React.Component<IEffectProps, {}> {

  componentDidMount() {
    const el = document.querySelector('.your-selector'); // Replace with actual selector
    if (!el) return;

    const props = ["position", "top", "bottom", "left", "right", "height", "width"];
    const mode = this.props.mode || "effect";
    const direction = this.props.direction || "left";
    const distance = this.props.distance || 20;
    const times = this.props.times || 3;
    const speed = Math.round(this.props.duration / (times * 2 + 1));

    $.effects.save(el, props);
    el.show();
    $.effects.createWrapper(el);

    // Animation logic
    for (let i = 0; i < times; i++) {
      let animation = {};
      let positiveMotion = direction === "up" || direction === "left";

      animation[direction === "up" || direction === "down" ? "top" : "left"] =
        positiveMotion ? "-=" + distance : "+=" + distance;
      
      el.animate(animation, speed, this.props.easing);

      if (i < times - 1) {
        let reverse = {};
        reverse[direction === "up" || direction === "down" ? "top" : "left"] =
          !positiveMotion ? "-=" + distance * 2 : "+=" + distance * 2;
        
        el.animate(reverse, speed, this.props.easing);
      }
    }
    
    // Restore original state
    $.effects.restore(el, props);
    $.effects.removeWrapper(el);
  }

  render() {
    return null; // Since the effect is handled in componentDidMount
  }
}

export default EffectComponent;