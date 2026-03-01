import React from 'react';
import api from '@/lib/api';  // Assuming this module uses axios under the hood

class MySpinnerComponent extends React.Component {
    private cancelBlur: boolean;
    
    constructor(props: any) {
        super(props);
        this.cancelBlur = false;  // Initialize your flag here
    }

    private _delay(callback: Function): void {
        setTimeout(() => callback.call(this), 500);  // Simulate a delay
    }
    
    private async _start(event: React.MouseEvent<HTMLDivElement, MouseEvent>): Promise<void> {
        if (this.cancelBlur) return;
        
        const response = await api.get('/some-endpoint');  // Fetch some data from API

        console.log(response.data);
    }

    private _stop(): void {
        this.cancelBlur = true;  // Example logic for stopping
    }
    
    private async checkFocus(event: React.FocusEvent<HTMLInputElement>): Promise<void> {
        if (this.cancelBlur) return;
        
        const response = await api.get('/some-endpoint');  // Fetch some data from API

        console.log(response.data);
    }

    render() {
        return (
            <div>
                {/* Your UI components here */}
                <input type="text" onBlur={e => this.checkFocus(e)} />
                <button onClick={(e) => { if (!this.cancelBlur) this._start(e); }}>Spin</button>
                <button onMouseUp={() => this._stop()}>Stop</button>
            </div>
        );
    }
}

export default MySpinnerComponent;