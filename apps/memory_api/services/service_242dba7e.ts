import api from '@/lib/api';

class DomWidgetService {
    constructor() {}

    private getPosition(element: HTMLElement): { x: number; y: number } {
        const rect = element.getBoundingClientRect();
        return { x: rect.left + window.scrollX, y: rect.top + window.scrollY };
    }

    private addClass(element: HTMLElement, className: string): void {
        if (!element.classList.contains(className)) {
            element.classList.add(className);
        }
    }

    private removeClass(element: HTMLElement, className: string): void {
        if (element.classList.contains(className)) {
            element.classList.remove(className);
        }
    }

    async pinElementWhenScroll(mainSelector: string, positionSelector: string, widthSelector: string): Promise<void> {
        const wrap = document.querySelector<HTMLElement>(mainSelector);
        const configWrap = document.querySelector<HTMLElement>(widthSelector);
        const panelHeading = document.querySelector<HTMLElement>(positionSelector);

        if (!wrap || !configWrap || !panelHeading) return;

        const wrapWidth = configWrap.clientWidth;
        
        this.observeScroll(mainSelector, positionSelector, wrapWidth);
    }

    private observeScroll(mainSelector: string, positionSelector: string, width: number): void {
        $(window).on("scroll", async () => {
            const panelHeadingPosition = await this.getPosition(document.querySelector<HTMLElement>(positionSelector));

            if (this.getWindowScrollY() > panelHeadingPosition.y) {
                const wrap = document.querySelector<HTMLElement>(mainSelector);
                this.addClass(wrap!, "fix-panel");
                wrap!.style.width = width + 'px';
            } else {
                const wrap = document.querySelector<HTMLElement>(mainSelector);
                this.removeClass(wrap!, "fix-panel");
                wrap!.style.width = 'auto';
            }
        });
    }

    private getWindowScrollY(): number {
        return window.scrollY;
    }
}

export default new DomWidgetService();