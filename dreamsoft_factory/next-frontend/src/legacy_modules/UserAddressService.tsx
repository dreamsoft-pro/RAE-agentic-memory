/**
 * Service: UserAddressService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface UserAddressServiceProps {
  userID: string;
}

const UserAddressService = ({ userID }: UserAddressServiceProps) => {
  const [addresses, setAddresses] = useState([]);
  const resource = useRef(`users/${userID}/address`);

  useEffect(() => {
    getAllAddresses();
  }, []);

  const getAllAddresses = async () => {
    try {
      const response = await axios.get(process.env.API_URL + resource.current + '?type=1');
      setAddresses(response.data);
    } catch (error) {
      console.error('Error fetching addresses:', error);
    }
  };

  const getAllAddressesVat = async () => {
    try {
      const response = await axios.get(process.env.API_URL + resource.current + '?type=2');
      setAddresses(response.data);
    } catch (error) {
      console.error('Error fetching addresses:', error);
    }
  };

  const createAddress = async (data: any) => {
    try {
      const response = await axios.post(process.env.API_URL + resource.current, data);
      if (response.data.response) {
        setAddresses([...addresses, response.data]);
      } else {
        console.error('Failed to create address:', response.data);
      }
    } catch (error) {
      console.error('Error creating address:', error);
    }
  };

  const editAddress = async (data: any) => {
    try {
      const response = await axios.put(process.env.API_URL + resource.current, data);
      if (response.data.response) {
        setAddresses(addresses.map(address => address.ID === data.ID ? response.data : address));
      } else {
        console.error('Failed to edit address:', response.data);
      }
    } catch (error) {
      console.error('Error editing address:', error);
    }
  };

  const removeAddress = async (addressID: string) => {
    try {
      await axios.delete(process.env.API_URL + resource.current + `/${addressID}`);
      setAddresses(addresses.filter(address => address.ID !== addressID));
    } catch (error) {
      console.error('Error removing address:', error);
    }
  };

  return null; // This component doesn't render anything, it just handles the logic for fetching and manipulating addresses.
};

export default UserAddressService;