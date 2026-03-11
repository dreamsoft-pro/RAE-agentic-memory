import { useEffect, useState } from 'react';
import axios from 'axios';
import NextRouter from 'next/router';

interface User {
  id?: string;
  super?: boolean;
}

const MyComponent: React.FC = () => {
  const [user, setUser] = useState<User | undefined>(undefined);
  const [logged, setLogged] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/data'); // Replace with actual endpoint
        if (response.data.user) {
          setUser(response.data.user);
        }

        if (user && user.super) {
          let startPoint = 'client-zone-orders';
          if (typeof window !== 'undefined' && window.localStorage.getItem('myZoneStartPoint')) {
            startPoint = window.localStorage.getItem('myZoneStartPoint')!;
          }
          
          NextRouter.push(startPoint).then(() => {
            setLogged(true);
            console.log('Login success');
          });
        } else {
          const defaultAddressResponse = await axios.get('/api/default-address'); // Replace with actual endpoint
          if (defaultAddressResponse.data.response) {
            const params = { addressID: defaultAddressResponse.data.address.ID };
            await axios.post('/api/update-default-address', params); // Replace with actual endpoint
          }
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, [user]);

  return (
    <div>
      {logged ? (
        <p>Welcome, logged in user!</p>
      ) : (
        <p>Not logged in.</p>
      )}
    </div>
  );
};

export default MyComponent;