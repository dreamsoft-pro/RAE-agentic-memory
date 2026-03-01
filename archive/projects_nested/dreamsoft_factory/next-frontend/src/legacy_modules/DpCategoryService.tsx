/**
 * Service: DpCategoryService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { createContext, useContext, useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';
import styled from 'styled-components';

const API_URL = process.env.REACT_APP_API_URL;

interface DpCategoryServiceProps {
  children: React.ReactNode;
}

interface Category {
  id: number;
  name: string;
  // Add other properties as needed
}

const DpCategoryContext = createContext<{
  categories: Category[];
  setCategories: (categories: Category[]) => void;
}>({
  categories: [],
  setCategories: () => {},
});

export const useDpCategory = () => useContext(DpCategoryContext);

const DpCategoryService: React.FC<DpCategoryServiceProps> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${API_URL}/dp_categories/forViewPublic/1`);
        setCategories(response.data);
      } catch (error) {
        console.error("Error fetching categories:", error as AxiosError);
      }
    };

    fetchData();
  }, []);

  return (
    <DpCategoryContext.Provider value={{ categories, setCategories }}>
      {children}
    </DpCategoryContext.Provider>
  );
};

const Container = styled.div`
  padding: 20px;
`;

const CategoryList = () => {
  const { categories } = useDpCategory();

  return (
    <Container>
      <h1>Categories</h1>
      <ul>
        {categories.map(category => (
          <li key={category.id}>{category.name}</li>
        ))}
      </ul>
    </Container>
  );
};

export default DpCategoryService;