import api from '@/lib/api';

class VolumeService {
  private resource: string;
  private groupID: string;

  constructor(resource: string, groupID: string) {
    this.resource = resource;
    this.groupID = groupID;
  }

  public async setStepVolume(stepVolume: any): Promise<any> {
    try {
      const response = await api.post(this.resource + '/setStepVolume', { stepVolume });
      if (response.data.response) {
        PsTypeService.cacheRemove(this.groupID);
        return response.data;
      } else {
        throw new Error('Failed to set step volume');
      }
    } catch (error: any) {
      throw error;
    }
  }

  public async setFormats(formatID: string, formats: any): Promise<any> {
    try {
      const response = await api.patch(this.resource + '/' + formatID + '/formats', { formats });
      if (response.data.response) {
        PsTypeService.cacheRemove(this.resource);
        return response.data;
      } else {
        throw new Error('Failed to set formats');
      }
    } catch (error: any) {
      throw error;
    }
  }

  // Assuming cache remove and other methods are defined in PsTypeService
}

// Example usage:
const service = new VolumeService('example-resource', '123456');

service.setStepVolume({ volumeValue: 0.5 }).then(data => console.log(data)).catch(error => console.error(error));

service.setFormats('7890', [{ formatData }]).then(data => console.log(data)).catch(error => console.error(error));