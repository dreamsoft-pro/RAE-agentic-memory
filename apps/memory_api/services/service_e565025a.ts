import { useEffect } from 'react';
import api from '@/lib/api';

class SelectableComponent {
    private _trigger: (eventName: string, event: Event, data: any) => void;
    private selectee: { $element: HTMLElement; selected?: boolean; selecting?: boolean; unselecting?: boolean; startselected?: boolean } = {
        $element: document.createElement('div'),
        selected: false,
        selecting: false,
        unselecting: false,
        startselected: false
    };

    private processSelection(hit: boolean, event: Event) {
        if (hit) {
            // SELECT
            if (this.selectee.selected) {
                this.selectee.$element.classList.remove("ui-selected");
                this.selectee.selected = false;
            }
            if (this.selectee.unselecting) {
                this.selectee.$element.classList.remove("ui-unselecting");
                this.selectee.unselecting = false;
            }
            if (!this.selectee.selecting) {
                this.selectee.$element.classList.add("ui-selecting");
                this.selectee.selecting = true;
                // selectable SELECTING callback
                this._trigger("selecting", event, { selecting: this.selectee.element });
            }
        } else {
            // UNSELECT
            if (this.selectee.selecting) {
                if ((event.metaKey || event.ctrlKey) && this.selectee.startselected) {
                    this.selectee.$element.classList.remove("ui-selecting");
                    this.selectee.selecting = false;
                    this.selectee.$element.classList.add("ui-selected");
                    this.selectee.selected = true;
                } else {
                    this.selectee.$element.classList.remove("ui-selecting");
                    this.selectee.selecting = false;
                    if (this.selectee.startselected) {
                        this.selectee.$element.classList.add("ui-unselecting");
                        this.selectee.unselecting = true;
                    }
                    // selectable UNSELECTING callback
                    this._trigger("unselecting", event, { unselecting: this.selectee.element });
                }
            }
            if (this.selectee.selected) {
                if (!event.metaKey && !event.ctrlKey && !this.selectee.startselected) {
                    this.selectee.$element.classList.remove("ui-selected");
                    this.selectee.selected = false;
                }
            }
        }
    }

    private _trigger(eventName: string, event: Event, data: any): void {
        // Implement the trigger logic as per your application's requirements
        console.log(`Event ${eventName} triggered with data:`, data);
    }
}

export default function Selectable() {
    useEffect(() => {
        const selectable = new SelectableComponent();
        document.body.addEventListener('click', (event) => {
            const hit = /* Determine if the event hits a selection */;
            selectable.processSelection(hit, event);
        });
    }, []);

    return <div>Selectable Component</div>;
}