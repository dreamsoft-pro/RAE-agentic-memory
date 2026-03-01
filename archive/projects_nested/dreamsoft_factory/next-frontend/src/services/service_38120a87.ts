import React, { Component } from 'react';
import api from '@/lib/api';

interface TabsProps {
    active?: number | null;
    collapsible?: boolean;
    event?: string;
    heightStyle?: string;
}

interface TabsState {
    tabs: any[];
    activeIndex: number;
    data: any[];
}

class Tabs extends Component<TabsProps, TabsState> {

    constructor(props: TabsProps) {
        super(props);
        
        this.state = {
            tabs: [],
            activeIndex: props.active ?? 0,
            data: []
        };
    }

    componentDidMount() {
        // Fetch data to populate the tabs here
        this.fetchData();
    }

    async fetchData() {
        try {
            const response = await api.get('/api/tabs'); // Replace with your actual API endpoint
            this.setState({ data: response.data, tabs: response.data.tabs });
        } catch (error) {
            console.error('Failed to fetch data', error);
        }
    }

    handleTabClick(index: number): void {
        if (!this.props.collapsible && index === this.state.activeIndex) return;
        
        // Toggle or activate the tab here
        this.setState({ activeIndex: index });
    }

    isLocal(anchor: string): boolean {
        const rhash = /#.*$/;

        try {
            anchor = decodeURIComponent(anchor.replace(rhash, ''));
        } catch (error) {}

        return anchor.length > 1 && anchor === location.href.replace(rhash, '');
    }

    render() {
        // Render the tabs and their content here based on state
        const { activeIndex, data } = this.state;

        return (
            <div>
                {data.map((tab, index) => (
                    <button key={index} onClick={() => this.handleTabClick(index)}>
                        {tab.title}
                    </button>
                ))}
                
                {/* Render the content of the currently active tab */}
                {this.renderActiveTabContent(activeIndex)}
            </div>
        );
    }

    renderActiveTabContent(active: number) {
        // Return the rendered content for the active tab
        const { tabs, data } = this.state;
        return (
            <div key={active}>
                {/* Render specific tab content here */}
                {tabs[active].content}
            </div>
        );
    }
}

export default Tabs;