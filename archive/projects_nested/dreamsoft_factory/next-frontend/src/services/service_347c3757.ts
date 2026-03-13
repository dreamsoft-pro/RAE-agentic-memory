import { useEffect } from 'react';
import api from '@/lib/api';

interface SelectableItem {
    $element: HTMLElement;
    selected?: boolean;
    startselected?: boolean;
    unselecting?: boolean;
}

class SelectComponent {
    private selectees: NodeListOf<Element>;
    private event: Event;

    constructor(selectees: NodeListOf<Element>, event: Event) {
        this.selectees = selectees;
        this.event = event;
    }

    private async handleUnselect() {
        for (const element of this.selectees) {
            const selecteeElement = element as HTMLElement;
            if (!element.dataset['selectable-item']) continue;

            let selectee: SelectableItem = JSON.parse(element.dataset['selectable-item']);
            selectee.startselected = true;

            if (!(this.event.metaKey || this.event.ctrlKey)) {
                selectee.$element = document.querySelector(selecteeElement.dataset.selectableItemId);
                selectee.selected = false;
                selectee.$element?.classList.remove('ui-selected');
                selectee.unselecting = true;
                selectee.$element?.classList.add('ui-unselecting');

                // selectable UNSELECTING callback
                this._trigger("unselecting", this.event, { unselecting: selecteeElement });
            }
        }
    }

    private _trigger(eventName: string, event: Event, data?: any) {
        console.log(`Event ${eventName} triggered with data`, data);
        // Implement your logic here to handle the trigger
    }
}

// Usage example in React component's useEffect or another lifecycle method
function useSelectableComponent(selecteesSelector: string, event: Event) {
    useEffect(() => {
        const selectees = document.querySelectorAll(selecteesSelector);
        if (selectees.length === 0) return;

        const selectComponent = new SelectComponent(selectees, event);
        selectComponent.handleUnselect();
    }, [event]);
}