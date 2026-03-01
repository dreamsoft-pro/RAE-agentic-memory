import api from "@/lib/api";

interface GlobalParamsInterface {
  [key: string]: any;
}

class DataFetcher {
  private globalParams: GlobalParamsInterface = {};

  addParam(key: string, value: any): void {
    this.globalParams[key] = value;
  }

  clearParams(): void {
    this.globalParams = {};
  }

  async getCommonData(statuses?: string[]): Promise<void> {
    try {
      const response = await api.get('/common-data', { params: { statuses } });
      // Process the response data here
      console.log(response.data);
    } catch (error) {
      console.error("Failed to fetch common data:", error);
    }
  }

  async fetchData(): Promise<void> {
    try {
      const resource = 'example-resource'; // Define as needed or derive from business logic
      const url = `${process.env.BASE_URL}/${resource}`;
      const response = await api.get(url, { params: this.globalParams });
      console.log(response.data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  }

  // Add other methods as necessary based on business logic
}

export default DataFetcher;