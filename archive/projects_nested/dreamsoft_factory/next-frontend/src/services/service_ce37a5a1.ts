import api from '@/lib/api';
import { useEffect, useState } from 'react';

interface LangServiceProps {
  resource: string;
  langCode?: string;
}

export default function useLangService({ resource, langCode = '' }: LangServiceProps) {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const response = await api.get(`${resource}/${langCode}`);
        if (response.data.response) {
          setData(response.data.response);
        } else {
          setError(new Error(JSON.stringify(response.data)));
        }
      } catch (err: any) {
        setError(err);
      }
    })();
  }, [resource, langCode]);

  const editLang = async (lang: object): Promise<void> => {
    try {
      await api.put(`${resource}`, lang);
      setData(await api.get(resource));
    } catch (error) {
      setError(error);
    }
  };

  const removeLang = async (id: string): Promise<void> => {
    try {
      await api.delete(`${resource}/${id}`);
      setData(await api.get(resource));
    } catch (error) {
      setError(error);
    }
  };

  return { data, error, editLang, removeLang };
}