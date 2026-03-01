import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface PagingSettings {
  currentPage: number;
  pageSize: number;
}

const getMyProjects = async (sortBy: string, order: string, pagingSettings: PagingSettings) => {
  const accessTokenName = 'YOUR_ACCESS_TOKEN_NAME_HERE'; // Define this constant or pass it as a parameter
  const resource = 'getMyProjects';
  const url = `${process.env.NEXT_PUBLIC_API_URL_EDITOR}/${resource}?sortBy=${sortBy}&order=${order}&page=${pagingSettings.currentPage}&display=${pagingSettings.pageSize}`;

  try {
    const response = await api.get(url, {
      headers: {
        [accessTokenName]: AuthService.readCookie(accessTokenName),
      },
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.log(error);
    throw error.response.status || error.message;
  }
};

const useReclamationSettings = () => {
  const [settings, setSettings] = useState<SettingService | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      const setting = new SettingService('reclamation');
      try {
        // Assuming you need to do something with the 'setting' here
        // For now, just setting it in state as an example.
        setSettings(setting);
      } catch (error) {
        console.log(error);
      }
    };

    fetchSettings();
  }, []);

  return settings;
};