import api from '@/lib/api';

class SliderComponent {
    private closestHandle: HTMLElement;
    private eventTarget: HTMLElement;
    private offset: { left: number; top: number };
    private mouseOverHandle: boolean;
    private clickOffset: { left: number; top: number };
    private handles: NodeListOf<Element>;
    private handleIndex: number;

    constructor(closestHandle: HTMLElement, eventTarget: HTMLElement) {
        this.closestHandle = closestHandle;
        this.eventTarget = eventTarget;
    }

    public mouseStart(event: MouseEvent): boolean {
        return true;
    }

    public async mouseDrag(event: MouseEvent): Promise<boolean> {
        const position = { x: event.pageX, y: event.pageY };
        const normValue = await this.normValueFromMouse(position);
        this.slideEvent(event, this.handleIndex, normValue);
        return false;
    }

    private isMouseOverHandle(): boolean {
        const $target = $(this.eventTarget);
        const $closestHandle = $(this.closestHandle);
        return !$target.parents().addBack().is($closestHandle);
    }

    private calculateClickOffset(): { left: number; top: number } {
        if (!this.isMouseOverHandle()) {
            const offset = this.closestHandle.getBoundingClientRect();
            const width = this.closestHandle.offsetWidth;
            const height = this.closestHandle.offsetHeight;

            return {
                left: event.pageX - offset.left - (width / 2),
                top: event.pageY - offset.top -
                    (height / 2) -
                    parseInt($(this.closestHandle).css('borderTopWidth'), 10) || 0 -
                    parseInt($(this.closestHandle).css('borderBottomWidth'), 10) || 0 +
                    parseInt($(this.closestHandle).css('marginTop'), 10) || 0
            };
        }
        return { left: 0, top: 0 };
    }

    private async slideEvent(event: MouseEvent, index: number, normValue: number): Promise<void> {
        // Implement the logic for _slide as per your requirements.
        console.log('Sliding handle to value:', normValue);
    }

    private normValueFromMouse(position: { x: number; y: number }): Promise<number> {
        // Placeholder implementation for normValueFromMouse
        return new Promise((resolve) => resolve(0.5));  // Example placeholder resolution.
    }
}