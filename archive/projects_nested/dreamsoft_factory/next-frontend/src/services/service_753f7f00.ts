import React from 'react';
import { useEffect } from 'react';
import api from '@/lib/api';

// Define the interface for data you expect to receive from your API.
interface MyData {
  id: number;
  name: string;
}

export default class MyComponent extends React.Component<{}, { items: MyData[] }> {

  constructor(props: {}) {
    super(props);
    this.state = { items: [] };
  }

  componentDidMount() {
    this.fetchData();
  }

  async fetchData(): Promise<void> {
    try {
      // Assuming the API returns a list of data in JSON format.
      const response = await api.get('/my-endpoint');
      if (response.data) {
        this.setState({ items: response.data });
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  }

  render(): JSX.Element {
    return (
      <div>
        {this.state.items.map(item => (
          <div key={item.id}>
            <h1>{item.name}</h1>
          </div>
        ))}
      </div>
    );
  }
}