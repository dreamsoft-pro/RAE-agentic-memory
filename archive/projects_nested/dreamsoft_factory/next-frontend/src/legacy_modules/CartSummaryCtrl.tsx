/**
 * Service: CartSummaryCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import Modal from 'react-modal';

const CartSummaryCtrl: React.FC<{ cart: any }> = ({ cart }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div>
      <button onClick={() => openModal()}>Open Delivery Method Modal</button>
      <Modal isOpen={isModalOpen} onRequestClose={closeModal}>
        <h2>Delivery Method</h2>
        <p>{JSON.stringify(cart)}</p>
        <button onClick={closeModal}>Close Modal</button>
      </Modal>
    </div>
  );
};

export default CartSummaryCtrl;
