import api from '@/lib/api';
import { useEffect, useRef } from 'react';

interface SlideEffectOptions {
  times: number;
  el: HTMLElement;
  animation1: string[];
  animation2?: string[]; // Optional if `animation` is used instead of this.
  speed: number;
  easing: string;
  mode: string;
  props: string[];
}

class Effects {
  async slideEffect(options: SlideEffectOptions, done: () => void) {
    const { times, el, animation1, animation2, speed, easing, mode, props } = options;

    // Define variables
    let i: number = 0;
    let queuelen: number = 1; // Example value, adjust as necessary

    // Shakes part of the effect
    for (i = 1; i < times; i++) {
      el.animate(animation1, speed, easing);
      el.animate(animation2 ? animation2 : [], speed, easing); // If `animation2` is not provided, use an empty array.
    }

    el
      .animate(animation1, speed, easing)
      .animate([ 'queue', [] ], speed / 2, easing) // Example queue animation, adjust as necessary
      .queue(() => {
        if (mode === "hide") {
          el.hide();
        }
        this.restoreProps(el, props);
        this.removeWrapper(el); // Assuming these are methods of the class.
        done();
      });

    if (queuelen > 1) {
      const queue = el.queue(); // Fetch current queue
      queue.splice.apply(queue,
        [ 1, 0 ].concat(
          queue.splice(queuelen, animation2 ? 3 : 2) // Adjust length based on whether `animation2` is used.
        )
      );
    }
    el.dequeue();
  }

  private restoreProps(element: HTMLElement, props: string[]): void {
    // Implementation to restore properties
    console.log('Restoring properties for:', element);
  }

  private removeWrapper(element: HTMLElement): void {
    // Implementation to remove wrapper
    console.log('Removing wrapper from:', element);
  }
}

// Example usage in a React component
function SlideEffectComponent() {
  const elRef = useRef(null);

  useEffect(() => {
    if (!elRef.current) return;

    const options: SlideEffectOptions = {
      times: 3,
      el: elRef.current as HTMLElement,
      animation1: ['animate', 'example'],
      speed: 500,
      easing: 'linear',
      mode: "hide",
      props: ['width', 'height'] // Example properties to restore
    };

    const effects = new Effects();
    
    (async () => {
      await effects.slideEffect(options, () => console.log('Animation complete'));
    })();
  }, []);

  return <div ref={elRef}>Animate me</div>;
}

export default SlideEffectComponent;