import api from "@/lib/api";
import { useEffect, useState } from "react";

type Event = any;

class SpinnerComponent extends React.Component<{}, {}> {
  private element: HTMLInputElement | null;
  private previous: string | null;
  private mousewheelTimer: number | null;

  constructor(props: {}) {
    super(props);
    this.element = null; // Ensure 'element' is defined before use
    this.previous = null; // Ensure 'previous' is defined before use
    this.mousewheelTimer = null; // Ensure 'mousewheelTimer' is defined before use
  }

  private _stop(event?: Event): void {
    console.log("Stop spinner");
    clearTimeout(this.mousewheelTimer);
    this.mousewheelTimer = null;
  }

  private _refresh(): void {
    if (this.element) {
      this.previous = this.element.value; // Ensure 'previous' is updated before use
    }
  }

  private _trigger(eventType: string, event?: Event): void {
    console.log(`Triggering ${eventType} event`);
  }

  private _start(event: Event): boolean {
    return true;
  }

  private _spin(step: number, event?: Event): void {
    console.log("Spinning with step", step);
  }

  private _delay(callback: () => void, delay: number = 100): number {
    return setTimeout(callback, delay);
  }

  private spinning: boolean = false;

  options: { step: number } = { step: 1 };

  componentDidMount() {
    this._refresh();
  }

  componentDidUpdate(prevProps: {}, prevState: {}) {
    if (this.element && prevProps !== this.props) {
      const currentValue = this.element.value;
      const previousValue = this.previous;

      if (currentValue !== previousValue) {
        this._trigger("change", null);
      }
    }
  }

  mousewheelHandler(event: Event, delta: number): void {
    if (!delta) return;

    if (!this.spinning && !this._start(event)) return false;

    this._spin((delta > 0 ? 1 : -1) * this.options.step, event);

    clearTimeout(this.mousewheelTimer);
    this.mousewheelTimer = this._delay(() => {
      if (this.spinning) {
        this._stop();
      }
    }, 100);

    event.preventDefault();
  }

  mousedownHandler(event: Event): void {
    const previousValue = this.previous;
  }
}