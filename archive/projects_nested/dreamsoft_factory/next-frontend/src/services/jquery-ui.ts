
// my-component.tsx

import React, { useEffect, useState } from 'react';
import axios from '@/lib/api'; // Assuming this module wraps Axios for API calls

class MyComponent extends React.Component<{}, { data: any }> {
    constructor(props: {}) {
        super(props);
        this.state = {
            data: null,
        };
    }

    componentDidMount() {
        this.fetchData();
    }

    async fetchData() {
        try {
            const response = await api.get('/some-endpoint');
            this.setState({ data: response.data });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    render() {
        if (!this.state.data) return <div>Loading...</div>;

        return (
            <div>
                <h1>Data from API</h1>
                {/* Render your component here based on this.state.data */}
            </div>
        );
    }
}

export default MyComponent;
