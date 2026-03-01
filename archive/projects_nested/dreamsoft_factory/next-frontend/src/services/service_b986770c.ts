import api from "@/lib/api";
import { useEffect, useState } from "react";

export default function CartJoinAddresses() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.post(
          `${process.env.AUTH_URL}/cart/joinAddresses`,
          { domainName: location.hostname },
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );

        setData(response.data);
      } catch (err) {
        setError(err.response ? err.response.data : err.message);
      }
    };

    fetchData();
  }, []);

  // Your component logic that uses data and error states
}

// If you want to convert this into a service class instead of React component, here's how:
class TokenService {
  private async joinAddresses(params: any) {
    try {
      const response = await api.post(
        `${process.env.AUTH_URL}/cart/joinAddresses`,
        { domainName: location.hostname },
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error.message;
    }
  }

  // You can use this method in your component or other parts of the application
}

export default TokenService;