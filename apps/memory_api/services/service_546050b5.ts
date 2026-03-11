import api from '@/lib/api';

class ScheduleService {
  private resource: string = 'yourResourceName'; // Define your resource here

  public async updateOngoings(data: any): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${this.resource}/updateOngoings`;
      const response = await api.post(url, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.response.data : error.message);
    }
  }

  public static getInstance(): ScheduleService {
    if (!ScheduleService.instance) {
      ScheduleService.instance = new ScheduleService();
    }
    return ScheduleService.instance;
  }

  private constructor() {}
}

export default ScheduleService;