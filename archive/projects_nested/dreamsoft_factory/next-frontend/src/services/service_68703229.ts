import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';
import { useEffect, useState } from 'react';

interface Credentials {
  username: string;
  password: string;
}

interface AuthServiceResponse {
  user: {
    super: number;
  };
}

const LoginWidgetService = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const login = async (credentials: Credentials, backTo?: string) => {
    if (!Object.keys(credentials).length) {
      console.error('Unexpected error');
      return;
    }

    try {
      const response = await axios.post('/api/login', credentials);
      console.log('AuthService.login response', response.data);

      // Simulate the setting of user data and token
      setIsLoggedIn(true);

    } catch (error) {
      console.error(error);
    }
  };

  return { login };
};

export default LoginWidgetService;