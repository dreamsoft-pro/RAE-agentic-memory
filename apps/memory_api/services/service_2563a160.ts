import api from '@/lib/api';

class PositionCalculator {
    private offset: any;
    private scrollParent: HTMLElement;

    constructor(offset: any, scrollParent: HTMLElement) {
        this.offset = offset;
        this.scrollParent = scrollParent;
    }

    async _generatePosition(event: MouseEvent): Promise<{ top: number; left: number }> {
        const pos = { top: event.clientY, left: event.clientX };
        const mod = 1;

        return {
            top: (
                pos.top +
                (this.offset.relative?.top ?? 0) * mod +
                (this.offset.parent?.top ?? 0) * mod -
                ((this.cssPosition === "fixed" ? -this.scrollParent.scrollTop : document.scrollingElement.scrollTop) * mod)
            ),
            left: (
                pos.left +
                (this.offset.relative?.left ?? 0) * mod +
                (this.offset.parent?.left ?? 0) * mod -
                ((this.cssPosition === "fixed" ? -this.scrollParent.scrollLeft : document.scrollingElement.scrollLeft) * mod)
            )
        };
    }
}

// Usage example
const calculator = new PositionCalculator({ relative: { top: 10, left: 20 }, parent: { top: 5, left: 3 } }, document.documentElement);
calculator._generatePosition(new MouseEvent('click', { clientX: 100, clientY: 150 }))
    .then(position => console.log(position));