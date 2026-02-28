import { useRef } from 'react';
import api from '@/lib/api';

interface TooltipProps {
    target: HTMLElement;
}

class TooltipComponent extends React.Component<TooltipProps> {
    private tooltipDataRef = useRef<{ tooltip: any; closing: boolean }>({ tooltip: null, closing: false });
    private delayedShowIntervalId?: number;

    constructor(props: TooltipProps) {
        super(props);
        this.tooltipDataRef.current.closing = false;
    }

    componentWillUnmount() {
        // Clear the interval for delayed tracking tooltips
        if (this.delayedShowIntervalId !== undefined) {
            clearInterval(this.delayedShowIntervalId);
        }
    }

    open = async () => {
        const tooltipData = this.tooltipDataRef.current;

        if (!tooltipData.closing) {
            return;
        }

        // Simulate a jQuery target.removeData("ui-tooltip-open");
        this.tooltipDataRef.current = { ...this.tooltipDataRef.current, closing: false };

        // Clear the interval for delayed tracking tooltips
        clearInterval(this.delayedShowIntervalId);

        const tooltip = await api.getTooltip();  // Example API call to fetch tooltip data

        if (tooltip) {
            this.tooltipDataRef.current.tooltip = tooltip;
            this._removeDescribedBy();
        }
    }

    private _removeDescribedBy(target: HTMLElement): void {
        target.removeAttribute('aria-describedby');
    }
}

export default TooltipComponent;