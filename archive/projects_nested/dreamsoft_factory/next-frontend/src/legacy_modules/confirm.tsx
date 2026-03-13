/**
 * Service: confirm
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import './confirm.css'; // Assuming you have a corresponding CSS file for styling

interface ConfirmProps {
  title: string;
  description: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const Confirm: React.FC<ConfirmProps> = ({ title, description, onConfirm, onCancel }) => {
  return (
    <Modal show={true} onHide={onCancel}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div dangerouslySetInnerHTML={{ __html: description }} />
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onCancel}>
          {{ 'cancel' | translate }}
        </Button>
        <Button variant="success" onClick={onConfirm}>
          <i className="fa fa-check"></i> {{ 'submit' | translate }}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default Confirm;