import api from '@/lib/api';

class VolumeService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async removeRtDetails(volume, item): Promise<void> {
    const resource = `${this.resource}/${volume.volume}/ps_rt_details`;
    
    try {
      await api.delete(`${resource}/${item.details.ID}`);
    } catch (error) {
      throw error;
    }
  }

  public async setInvisible(volume): Promise<void> {
    const resource = `${this.resource}/${volume.volume}`;
    
    try {
      // Assuming you need to perform some operation here
      // For the sake of example, let's assume we're updating a property
      await api.put(`${resource}/invisible`, { invisible: true });
    } catch (error) {
      throw error;
    }
  }
}