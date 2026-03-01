import React, { PureComponent } from 'react';
import api from '@/lib/api'; // Assuming you have this setup in your project

class DataFetcher extends PureComponent<{}, { data: any }> {
    state = {
        data: null,
    };

    async componentDidMount() {
        try {
            const result = await api.get('/your-endpoint');
            this.setState({ data: result.data });
        } catch (error) {
            console.error('Failed to fetch data', error);
        }
    }

    render() {
        return (
            <div>
                {this.state.data ? (
                    <pre>{JSON.stringify(this.state.data, null, 2)}</pre>
                ) : (
                    <p>Loading...</p>
                )}
            </div>
        );
    }
}

export default DataFetcher;