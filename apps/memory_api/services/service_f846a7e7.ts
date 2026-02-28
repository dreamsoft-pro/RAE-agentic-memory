import React from 'react';
import axios from '@/lib/api'; // Importing custom API wrapper instead of Axios

class TooltipComponent extends React.Component {
    private element: HTMLElement;
    private options: { items: string };

    constructor(props: any) {
        super(props);
        this.options = { items: '[data-ui-tooltip]' };
    }

    componentDidMount() {
        this.removeTitleAttributes();
    }

    componentWillUnmount() {
        this.restoreTitleAttributes();
    }

    removeTitleAttributes(): void {
        const elements = Array.from(this.element.querySelectorAll(this.options.items));
        elements.forEach(element => {
            if (element.getAttribute('title')) {
                element.setAttribute('data-ui-tooltip-title', element.getAttribute('title'));
                element.removeAttribute('title');
            }
        });
    }

    restoreTitleAttributes(): void {
        const elements = Array.from(this.element.querySelectorAll(this.options.items));
        elements.forEach(element => {
            const storedTitle = element.getAttribute('data-ui-tooltip-title');
            if (storedTitle) {
                element.setAttribute('title', storedTitle);
                element.removeAttribute('data-ui-tooltip-title'); // Optionally clear after restore
            }
        });
    }

    open(event: React.MouseEvent): void {
        const target = event.target instanceof Element ? this.closest(target, this.options.items) : null;

        if (!target || target.getAttribute('data-ui-tooltip-id')) {
            return;
        }

        this.showTooltip(target);
    }

    private closest(element: HTMLElement | Node, selector: string): HTMLElement | null {
        let node = element as HTMLElement;
        while (node && !node.matches(selector)) {
            node = node.parentElement;
        }
        return node ? node : null;
    }

    private async showTooltip(target: HTMLElement): Promise<void> {
        // Example of using the custom API wrapper
        try {
            const response = await axios.get('/api/data');
            console.log(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}