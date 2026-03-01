import { useEffect } from 'react';
import api from '@/lib/api';

interface WindowEventHandlers {
    wrap: HTMLDivElement | null;
    configWrap: HTMLElement | null;
    position: { x: number; y: number };
}

export default class ResizeHandler extends React.Component<{}, WindowEventHandlers> {
    constructor(props: {}) {
        super(props);
        this.state = {
            wrap: null,
            configWrap: null,
            position: { x: 0, y: 0 },
        };
    }

    componentDidMount() {
        this.setState({
            wrap: document.getElementById('wrap') as HTMLDivElement | null,
            configWrap: document.querySelector('.config-wrap') as HTMLElement | null,
            position: getPosition(document.body),
        });
        window.addEventListener('resize', this.handleResize);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.handleResize);
    }

    handleResize = () => {
        const { wrap, configWrap } = this.state;
        if (!wrap || !configWrap) return;

        const wrapWidth = configWrap.clientWidth;
        if (window.scrollY > this.state.position.y) {
            wrap.style.width = `${wrapWidth}px`;
        }
    };

    getPosition(element: HTMLElement | null): { x: number; y: number } {
        let xPosition = 0, yPosition = 0;

        while (element !== null) {
            xPosition += element.offsetLeft - element.scrollLeft + element.clientLeft;
            yPosition += element.offsetTop - element.scrollTop + element.clientTop;
            element = element.offsetParent as HTMLElement | null;
        }

        return { x: xPosition, y: yPosition };
    }

    hasClass(element: HTMLElement, className: string): boolean {
        return !!element.className.match(new RegExp(`(\\s|^)${className}(\\s|$)`));
    }

    addClass(element: HTMLElement, className: string): void {
        if (!this.hasClass(element, className)) element.classList.add(className);
    }
}