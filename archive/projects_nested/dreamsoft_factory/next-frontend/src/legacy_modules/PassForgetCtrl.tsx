/**
 * Service: PassForgetCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { AuthService, Notification, UserService } from '@services';

const PassForgetCtrl = () => {
  const [email, setEmail] = useState('');
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const data = await UserService.passForget(email);
      if (data.response) {
        Notification.success("new_password_sent");
        router.push('/login');
      } else {
        Notification.error("error");
      }
    } catch (error) {
      Notification.error("error");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        required
      />
      <button type="submit">Send Password Reset</button>
    </form>
  );
};

export default PassForgetCtrl;
