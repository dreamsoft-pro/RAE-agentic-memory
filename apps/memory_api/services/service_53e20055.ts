import api from '@/lib/api';
import { FC, useEffect, useState } from 'react';

// Define a functional component or use a class if you must
class DataFetcher extends React.Component<{}, { data: any }> {
  constructor(props: {}) {
    super(props);
    this.state = {
      data: null,
    };
  }

  async componentDidMount() {
    try {
      const response = await api.get('/data-endpoint'); // Adjust the endpoint as necessary
      this.setState({ data: response.data });
    } catch (error) {
      console.error("Failed to fetch data", error);
    }
  }

  render() {
    if (!this.state.data) return <div>Loading...</div>;
    
    return (
      <div>
        {JSON.stringify(this.state.data)}
      </div>
    );
  }
}

export default DataFetcher;