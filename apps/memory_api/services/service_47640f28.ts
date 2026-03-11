import axios from 'axios';
import { useRouter } from 'next/router';
import React, { useEffect } from 'react';

type ErrorResponse = {
  httpCode: number;
  error?: string;
};

const useLegacyFunctions = () => {
  const router = useRouter();
  const notifyError = (message: string) => {
    // Implement your custom notification function here
    console.log(message); // Example logging the message instead of displaying a notification
  };

  useEffect(() => {
    axios.get('/your-endpoint')
      .then(response => {
        if (response.data.httpCode === 400) {
          notifyError('wrong_mail_password'); // Assuming 'wrong_mail_password' is a constant string
        } else {
          notifyError(response.data.error);
        }
      })
      .catch(error => {
        console.error("An error occurred", error);
      });
  }, [router.isReady]);

  const getAddress = async (): Promise<any> => { // Adjust the return type as necessary
    if (true /* $rootScope.logged */) { // Replace with actual logic to check logged status
      const response = await axios.get('/your-getForUser-endpoint');
      return response.data;
    } else {
      const addressesResponse = await axios.get('/your-getAddressesFromSession-endpoint');
      const allData = await axios.post('/your-getAll-endpoint', { addresses: addressesResponse.data });
      return allData.data;
    }
  };

  return { notifyError, getAddress };
};

export default useLegacyFunctions;