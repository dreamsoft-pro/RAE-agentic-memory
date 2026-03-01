/**
 * Service: client-zone-questions
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Order {
  name: string;
  calcID: string;
}

interface Props {
  order: Order;
  translate: (key: string) => string;
}

const ClientZoneQuestions: React.FC<Props> = ({ order, translate }) => {
  return (
    <div>
      <h3>{order.name}</h3>
      <div className="row">
        <div className="col-md-2">
          <b>{translate('name')}</b>
          <br />
          {order.name}
        </div>
        <div className="col-md-2">
          <b>{translate('calc_number')}</b>
          <br />
          {order.calcID}
        </div>
      </div>
    </div>
  );
};

export default ClientZoneQuestions;