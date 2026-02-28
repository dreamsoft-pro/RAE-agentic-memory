import React from 'react';
import api from '@/lib/api';

interface SliderProps {
  // Define props if needed
}

export default class MySlider extends React.Component<SliderProps> {
  private _slide(event: any, index: number, newVal: number): void {
    console.log('Sliding to new value:', newVal);
    // Handle sliding logic here
  }

  private _keyup(event: KeyboardEvent): void {
    const index = $(event.target).data("ui-slider-handle-index");

    if (this._keySliding) {
      this._keySliding = false;
      this._stop(event, index);
      this._change(event, index);
      $(event.target).removeClass('ui-state-active');
    }
  }

  private _keySliding: boolean = false; // Ensure all variables are defined before use
  private _stop(event: any, index: number): void {
    console.log('Stop sliding at:', index);
  }

  private _change(event: any, index: number): void {
    console.log('Change slider value to:', index);
    const url = '/api/slider'; // Example API endpoint URL
    try {
      const response = await api.put(url); // Assuming 'put' is a method in your @/lib/api module
      console.log(response.data);
    } catch (error) {
      console.error('Error updating slider:', error);
    }
  }

  componentDidMount() {
    $(this.el).on('slide', this._slide.bind(this));
    $(this.el).on('keyup', this._keyup.bind(this));
  }

  componentWillUnmount() {
    $(this.el).off('slide');
    $(this.el).off('keyup');
  }

  render(): JSX.Element {
    return <div ref={(el) => { this.el = el; }} className="slider"></div>;
  }
}