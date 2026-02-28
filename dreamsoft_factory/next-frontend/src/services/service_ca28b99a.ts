import api from '@/lib/api';

export async function removeRealizationTime(groupID: string, typeID: string, item: any): Promise<any> {
  if (!item.details) {
    return reject();
  }

  const resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_rt_details';
  const url = `/${item.details.ID}`;

  try {
    const response = await api.put(`${resource}/${url}`, null);
    if (response.response) {
      return resolve(response);
    } else {
      return reject(response);
    }
  } catch (error) {
    return reject(error);
  }
}