import api from '@/lib/api';
import { useEffect, useState } from 'react';

interface ProgressBarProps {
    value?: number;
    options: {
        max: number;
        completeCallback: () => void;
    };
}

export default class ProgressBar extends React.Component<ProgressBarProps> {

    private elementRef = React.createRef<HTMLDivElement>();
    private overlayDivRef = React.createRef<HTMLDivElement>();

    constructor(props) {
        super(props);
        this.state = { value: props.value || 0, oldValue: 0 };
    }

    componentDidMount() {
        const { options } = this.props;
        if (this.elementRef.current && options.autoRefresh) {
            // Simulate auto-refresh logic here
        }
    }

    componentDidUpdate(prevProps: ProgressBarProps) {
        if (prevProps.value !== this.props.value) {
            this.updateProgress(this.props.value);
        }
    }

    updateProgress(value: number) {
        const { indeterminate, options } = this.props;
        let element = this.elementRef.current;

        if (indeterminate) {
            element?.removeAttribute("aria-valuenow");
            // Assuming overlayDiv is part of the DOM structure when needed
            if (!this.overlayDivRef.current) {
                this.overlayDivRef.current = document.createElement('div');
                this.overlayDivRef.current.className = 'ui-progressbar-overlay';
                this.elementRef.current?.appendChild(this.overlayDivRef.current);
            }
        } else {
            element?.setAttribute("aria-valuemax", options.max.toString());
            element?.setAttribute("aria-valuenow", value.toString());

            if (this.overlayDivRef.current) {
                this.overlayDivRef.current.remove();
                this.overlayDivRef.current = null;
            }
        }

        const oldValue = this.state.oldValue;
        if (oldValue !== value) {
            this.setState({ oldValue: value }, () => this.triggerChange());
        }

        if (value === options.max && options.completeCallback) {
            options.completeCallback();
        }
    }

    triggerChange() {
        // Trigger change event logic
    }

    render() {
        return (
            <div ref={this.elementRef} style={{ width: "100%", height: '2em', background: '#ddd' }}>
                {/* Progress bar rendering goes here */}
            </div>
        );
    }
}