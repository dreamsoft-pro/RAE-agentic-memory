import api from '@/lib/api';

class MailTypeService {

  static async removeVariable(mailTypeID: number, variableID: number): Promise<void> {
    const url = `${process.env.API_URL}/${resource}/${mailTypeID}/mailVariables/${variableID}`;
    try {
      await api.delete(url);
    } catch (error) {
      throw error;
    }
  }

  static async editVariable(mailTypeID: number, data: any): Promise<any> {
    const url = `${process.env.API_URL}/${resource}/${mailTypeID}/mailVariables`;
    try {
      return await api.put(url, data);
    } catch (error) {
      throw error;
    }
  }

  static async getVariables(mailTypeID: number): Promise<any[]> {
    if (!resource) {
      throw new Error('Resource is not defined');
    }
    const url = `${process.env.API_URL}/${resource}/${mailTypeID}/mailVariables`;
    try {
      return await api.get(url);
    } catch (error) {
      throw error;
    }
  }

}

// Ensure resource is defined before using it
MailTypeService.resource = 'your-resource-name-here';

export default MailTypeService;