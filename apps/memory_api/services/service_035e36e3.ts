import React from 'react';
import api from '@/lib/api';

interface SelectableState {
    selecting: boolean;
    unselecting: boolean;
}

class Selectable extends React.Component<{}, SelectableState> {
    constructor(props: {}) {
        super(props);
        this.state = { selecting: false, unselecting: false };
    }

    _mouseStart(event: React.MouseEvent) {
        const selectee: any = {}; // Define your selectee object as needed
        selectee.unselecting = false;
        
        if (this._trigger("selecting", event, { selecting: selectee }) === false) {
            selectee.$element.addClass('ui-unselecting');
            selectee.unselecting = true;
            
            this._trigger("unselecting", event, {
                unselecting: selectee.element
            });
        }
    }

    _mouseStop(event: React.MouseEvent): void {
        this.setState({ dragged: false });
    }

    async fetchData() {
        try {
            const response = await api.get('/some-endpoint');
            console.log(response.data);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    }

    _trigger(eventName: string, event: React.MouseEvent, eventData?: any): boolean | void {
        // Implement your trigger logic here
    }

    render() {
        return <div>Selectable Component</div>;
    }
}

export default Selectable;