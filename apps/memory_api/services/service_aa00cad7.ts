import React from 'react';
import api from '@/lib/api';

interface SliderProps {
  options: any;
}

class Slider extends React.Component<SliderProps> {
  private _keySliding: boolean = false;

  handleKeyPress = (event: KeyboardEvent) => {
    const keyCode = event.keyCode;
    switch (keyCode) {
      case $.ui.keyCode.HOME:
      case $.ui.keyCode.END:
      case $.ui.keyCode.PAGE_UP:
      case $.ui.keyCode.PAGE_DOWN:
      case $.ui.keyCode.UP:
      case $.ui.keyCode.RIGHT:
      case $.ui.keyCode.DOWN:
      case $.ui.keyCode.LEFT: {
        event.preventDefault();
        if (!this._keySliding) {
          this._keySliding = true;
          $(event.target).addClass("ui-state-active");
          const allowed = this._start(event, keyCode);
          if (allowed === false) {
            return;
          }
        }
        break;
      }
    }

    const step = this.options.step;
    let curVal: number | any[] = [];
    let newVal: number | any[];

    if (this.options.values && Array.isArray(this.options.values)) {
      [curVal, newVal] = this.getValues(keyCode);
    } else {
      curVal = newVal = this.getValue();
    }
  }

  private _start(event: KeyboardEvent, index: number): boolean | void {
    // Implement logic for start event
  }

  private getValues(index: number): [number[], number[]] {
    return [this.values(index), this.values(index)];
  }

  private getValue(): number {
    return this.value();
  }
}