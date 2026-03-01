import api from '@/lib/api';

class EffectAnimator {
  private el: HTMLElement;
  private props: string[];
  private ref: string;
  private distance: number | undefined;
  private show: boolean;
  private hide: boolean;
  private motion: boolean;
  private times: number;

  constructor(el: HTMLElement, props: string[], ref: string, distance?: number) {
    this.el = el;
    this.props = props;
    this.ref = ref;
    this.distance = distance || undefined;
    this.show = false; // Initialize based on your logic
    this.hide = false; // Initialize based on your logic
    this.motion = false; // Initialize based on your logic
    this.times = 1; // Initialize based on your logic

    el.style.display = 'block'; // Show element
    this.createWrapper(el); // Create wrapper if needed
  }

  private saveState(): void {
    // Implement saving of state as per your requirements using props array
  }

  private createWrapper(el: HTMLElement): void {
    // Implement creating a wrapper for the element
  }

  public animateElements(speed: number, easing?: string): Promise<void> {
    return new Promise(async (resolve) => {
      this.saveState();

      const downAnim = {};
      if (!this.distance) {
        this.distance = this.el[this.ref === "top" ? "offsetHeight" : "offsetWidth"] / 3;
      }

      if (this.show) {
        downAnim['opacity'] = 1;
        downAnim[this.ref] = 0;

        // Show animation logic
        await new Promise((resolveShow) => {
          this.el.style.opacity = '0';
          const initialPosition = `${this.ref}: ${this.motion ? -2 * this.distance : 2 * this.distance}px`;
          this.el.style.cssText += `;${initialPosition}`;
          
          this.animate(downAnim, speed, easing).then(resolveShow);
        });
      }

      if (this.hide) {
        this.distance /= Math.pow(2, this.times - 1);
      }

      downAnim[this.ref] = 0;

      for (let i = 0; i < this.times; i++) {
        const upAnim = {};
        upAnim[this.ref] = `${this.motion ? "-=" : "+="} ${this.distance}px`;

        await this.animate(upAnim, speed, easing);
        await this.animate(downAnim, speed, easing);
      }

      resolve();
    });
  }

  private animate(animation: Record<string, any>, duration: number, easing?: string): Promise<void> {
    return new Promise((resolve) => {
      const effectPromise = new Promise((resolveAnimate) => {
        if (easing && typeof this.el.animate === 'function') {
          this.el.animate(
            [{ opacity: 0 }, { ...animation }],
            { duration, easing }
          ).onfinish = resolveAnimate;
        } else {
          // Fallback for browsers without native animate support
          const animationProperties: string[] = Object.keys(animation);
          let currentValues: Record<string, number> = {};

          const stepCallback = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;

            const progress = timestamp - startTimestamp;
            let complete = progress / duration > 1 ? 1 : progress / duration;

            for (let i = 0; i < animationProperties.length; i++) {
              const property = animationProperties[i];
              const value = this.calculateValue(property, currentValues[property], animation[property], complete);

              if (!currentValues[property]) {
                currentValues[property] = this.getStyle(this.el, property);
              }

              this.setStyle(this.el, property, value);
            }

            if (complete < 1) requestAnimationFrame(stepCallback);
            else resolveAnimate();
          };

          let startTimestamp: number | undefined;
          stepCallback(timestamp || performance.now()); // Start animation
        }
      });

      return effectPromise;
    });
  }

  private calculateValue(property: string, startValue: number | null, endValue: any, progress: number): number {
    if (startValue === null) return parseFloat(endValue);
    const type = typeof endValue;

    switch (type) {
      case 'number':
        return startValue + (endValue - startValue) * progress;
      case 'string':
        if (endValue[0] === '<') return startValue - (startValue / Number(endValue.slice(1)));
        else if (endValue[0] === '+') return startValue + parseFloat(endValue);
        else if (endValue[0] === '-') return startValue - parseFloat(endValue.slice(1));
      default:
        throw new Error(`Unsupported value type for property ${property}: ${type}`);
    }
  }

  private getStyle(el: HTMLElement, prop: string): number {
    // Implement logic to get the style of an element
    return Number(getComputedStyle(el)[prop]);
  }

  private setStyle(el: HTMLElement, prop: string, value: number): void {
    el.style[prop] = `${value}px`; // Adjust based on actual property name (may need 'px' or no unit)
  }
}