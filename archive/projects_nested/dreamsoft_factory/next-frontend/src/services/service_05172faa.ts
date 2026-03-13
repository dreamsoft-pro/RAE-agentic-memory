import axios, { AxiosResponse } from 'axios';
import { FC, useState, useEffect } from 'next/types';

class TypePatternService {
  private apiUrl: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api/typepatterns'; // Example API URL

  public async fetchPatterns(): Promise<AxiosResponse> {
    try {
      const response = await axios.get(this.apiUrl);
      return response;
    } catch (error) {
      throw new Error('Failed to fetch patterns');
    }
  }

  constructor() {}

  static getInstance(): TypePatternService {
    if (!TypePatternService.instance) {
      TypePatternService.instance = new TypePatternService();
    }
    return TypePatternService.instance;
  }
}

export default function PatternsPage() {
  const [patterns, setPatterns] = useState<AxiosResponse | null>(null);

  useEffect(() => {
    TypePatternService.getInstance().fetchPatterns()
      .then(response => {
        setPatterns(response);
      })
      .catch(error => console.error('Error fetching patterns:', error));
  }, []);

  return (
    <div>
      {patterns ? (
        <pre>{JSON.stringify(patterns.data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}