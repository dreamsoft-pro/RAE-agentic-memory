import api from "@/lib/api";

class StyleService {
  private resource: string = "mainCssFile"; // Assuming this is where 'resource' should be defined

  public async getMainCssData(data: any): Promise<any> {
    try {
      const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, data);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error; // Ensure to handle errors properly
    }
  }

  // Assuming you want a method that returns the StyleService instance or exposes other methods,
  // here is an example of how it might look like:
  
  public static getInstance(): StyleService {
    return new StyleService();
  }
}

export default StyleService;