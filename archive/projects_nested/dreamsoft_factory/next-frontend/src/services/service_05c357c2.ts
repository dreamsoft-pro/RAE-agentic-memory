import { useEffect, useState } from 'react';
import axios from '@/lib/api'; // Assuming the axios instance is properly set up here

interface ResourceData {
  id: number;
  name: string;
}

export default class MyClassComponent extends React.Component<{}, { data: ResourceData[] }> {

  constructor(props: {}) {
    super(props);
    this.state = { data: [] };
  }

  async componentDidMount() {
    try {
      const resourceUrl = '/api/resource'; // Define the URL properly before use
      const response = await axios.get<ResourceData[]>(resourceUrl); // Use TypeScript for type safety
      this.setState({ data: response.data });
    } catch (error) {
      console.error('Failed to fetch resources:', error);
    }
  }

  render() {
    return (
      <div>
        {this.state.data.map(item => (
          <div key={item.id}>
            <h3>{item.name}</h3>
          </div>
        ))}
      </div>
    );
  }
}