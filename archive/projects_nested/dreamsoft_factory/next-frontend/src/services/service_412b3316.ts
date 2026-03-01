import api from '@/lib/api';

export default class NewsService {

  private getResource(): string {
    return 'dp_news';
  }

  public async getRss(data: any): Promise<any> {
    const resource = this.getResource();
    const url = `${api.API_URL}/${resource}/rss`;

    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

}