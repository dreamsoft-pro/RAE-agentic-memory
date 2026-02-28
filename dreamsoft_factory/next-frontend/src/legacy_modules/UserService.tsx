/**
 * Service: UserService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect } from 'react';
import axios from 'axios';

const UserService = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const resource = 'users';

  useEffect(() => {
    const fetchData = async (force: boolean) => {
      if (!data || force) {
        try {
          const response = await axios.get(`${API_URL}/${resource}`);
          setData(response.data);
        } catch (err) {
          setError(err);
        }
      } else {
        // Return cached data if available and not forced
        setData(data);
      }
    };

    fetchData(false);
  }, [data]);

  const addUser = async (user: any) => {
    try {
      const response = await axios.post(`${API_URL}/${resource}`, user);
      if (response.data.response) {
        setData(response.data);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  const editUser = async (user: any) => {
    try {
      const response = await axios.patch(`${API_URL}/${resource}`, user);
      if (response.data.response) {
        // Invalidate cache or update as needed
        setData(response.data);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  const getGroups = async (user: any) => {
    try {
      const response = await axios.get(`${API_URL}/${resource}/${user.ID}/userGroups`);
      if (response.data.response) {
        // Invalidate cache or update as needed
        setData(response.data.items);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  const setGroups = async (user: any, items: any) => {
    try {
      const response = await axios.post(`${API_URL}/${resource}/${user.ID}/userGroups`, items);
      if (response.data.response) {
        // Invalidate cache or update as needed
        setData(response.data);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  const userRegister = async (data: any) => {
    try {
      const response = await axios.post(`${API_URL}/${resource}/register`, data);
      if (response.data.response) {
        setData(response.data);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  const getUserFtp = async () => {
    try {
      const response = await axios.get(`${API_URL}/${resource}/getUserFtpData`);
      return response.data;
    } catch (err) {
      setError(err);
    }
  };

  const getLoggedUserData = async () => {
    try {
      const response = await axios.get(`${API_URL}/${resource}/getLoggedUserData`);
      return response.data;
    } catch (err) {
      setError(err);
    }
  };

  const userDataChange = async (data: any) => {
    try {
      const response = await axios.post(`${API_URL}/${resource}/changeUserData`, data);
      if (response.data.response) {
        setData(response.data);
      } else {
        setError(response.data);
      }
    } catch (err) {
      setError(err);
    }
  };

  return {
    data,
    error,
    addUser,
    editUser,
    getGroups,
    setGroups,
    userRegister,
    getUserFtp,
    getLoggedUserData,
    userDataChange,
  };
};

export default UserService;