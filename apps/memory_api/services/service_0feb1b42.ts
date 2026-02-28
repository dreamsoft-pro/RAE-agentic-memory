import api from '@/lib/api';
import { useEffect } from 'react';

interface AnimationOptions {
  duration: number;
  easing?: string; // optional since it's not used as strictly required in the example snippet.
}

export default class EffectHandler {
  private el!: HTMLElement;
  private props!: string[];
  private mode!: string;

  constructor(element: HTMLElement, options: AnimationOptions) {
    this.el = element;
    this.props = ['border', 'margin']; // Example properties to restore
    this.mode = options.duration > 0 ? "show" : "hide";
  }

  public async animate(): Promise<void> {
    const o: AnimationOptions = { duration: 1000 }; // Example object with required duration.
    
    await new Promise((resolve) => {
      this.el.animate(
        { opacity: 'toggle' }, // Example animation property
        {
          queue: false,
          duration: o.duration,
          easing: o.easing || 'swing', // Default to swing if not provided
          complete: () => {
            if (this.mode === "hide") {
              this.el.style.display = 'none'; // Use native DOM manipulation for hide.
            }
            this.restoreStyles(); // Example method for restoring styles.
            resolve();
          },
        },
      );
    });
  }

  private restoreStyles(): void {
    // Placeholder implementation to mimic $.effects.restore
    console.log('Restoring original style properties');
    
    // Example of removing a wrapper class (if any)
    const wrapperClass = 'ui-wrapper';
    if (this.el.classList.contains(wrapperClass)) {
      this.el.classList.remove(wrapperClass);
    }
  }

  private done(): void {
    // Placeholder for the callback logic
    console.log('Animation completed');
  }
}

// Usage example in a Next.js component:
// const elementRef = useRef(null);

// useEffect(() => {
//   if (elementRef.current) {
//     const effectHandler = new EffectHandler(elementRef.current, { duration: 1000 });
//     effectHandler.animate().then(effectHandler.done.bind(effectHandler));
//   }
// }, [elementRef]);