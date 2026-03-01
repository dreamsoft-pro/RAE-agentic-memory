// src/components/MyApiComponent.ts

import React, { useEffect } from 'react';
import api from '@/lib/api'; // Assuming this is a valid import statement that wraps Axios or similar HTTP client.

interface MyData {
  key: string;
  value: number | string;
}

export default class MyApiComponent extends React.Component<{}, { data?: MyData[] }> {
  constructor(props: {}) {
    super(props);
    this.state = { data: undefined };
  }

  async componentDidMount() {
    try {
      const response = await api.get<MyData[]>('https://api.example.com/data');
      this.setState({ data: response.data });
    } catch (error) {
      console.error("Failed to fetch data", error);
    }
  }

  render() {
    return (
      <div>
        {this.state.data ? (
          this.state.data.map(item => (
            <div key={item.key}>
              <p>{item.value}</p>
            </div>
          ))
        ) : (
          <p>Loading...</p>
        )}
      </div>
    );
  }
}