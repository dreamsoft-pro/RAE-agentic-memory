import api from "@/lib/api";
import { useEffect, useState } from "react";

export default function OngoingService() {
  const [sortData, setSortData] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchOngoingsOrder = async () => {
      try {
        const response = await api.patch(`${resource}/ongoingsOrder`, sort);
        setSortData(response.data);
      } catch (err) {
        setError(err);
      }
    };

    // Assuming resource and sort are defined elsewhere in your application
    fetchOngoingsOrder();
  }, [sort]);

  return { sortData, error };
}