import React, { Component } from 'react';
import axios from '@your-project/lib/api'; // Assuming this is your custom axios wrapper

class SpinnerInput extends Component {
  private previousValue: string = '';
  private inputRef: HTMLInputElement | null = null;

  componentDidMount() {
    this.checkFocus();
  }

  componentDidUpdate(prevProps: Readonly<{}>, prevState: Readonly<{}>) {
    if (prevState.previousValue !== this.previousValue) {
      this.checkFocus();
    }
  }

  componentWillUnmount() {}

  private async checkFocus(): Promise<void> {
    const isActive = document.activeElement === this.inputRef;
    if (!isActive) {
      await this.setInputFocus();
      this.previousValue = this.inputRef?.value || '';
      // Ensure the previous value is set correctly after focus
      setTimeout(() => {
        this.previousValue = this.inputRef?.value || '';
      }, 0);
    }
  }

  private async setInputFocus(): Promise<void> {
    if (this.inputRef) {
      this.inputRef.focus();
    }
  }

  render() {
    return (
      <div>
        <input
          ref={(ref) => { this.inputRef = ref; }}
          type="text"
          onKeyDown={async (event: React.KeyboardEvent<HTMLInputElement>) => {
            event.preventDefault();
            await this.checkFocus();
          }}
        />
      </div>
    );
  }
}

export default SpinnerInput;