import React from 'react';
import { useState } from 'react';
import api from '@/lib/api';

type OrderType = {
  ID?: number;
  paymentID?: number;
  products: Array<{
    price: string | null;
    grossPrice: string | null;
  }>;
};

const MyComponent: React.FC<OrderType> = ({ order }) => {
  const [payments, setPayments] = useState([]);
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [preventPayment, setPreventPayment] = useState(false);

  const preparePrice = (price: string | null) => {
    // Implement the logic for preparing price
    return price;
  };

  const getDeliveryPrice = async (order: OrderType): Promise<void> => {
    // Implement this function based on business requirements
  };

  const getPayments = async (orderId: number): Promise<any[]> => {
    try {
      const response = await api.get(`/payments?order_id=${orderId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching payments:', error);
      return [];
    }
  };

  React.useEffect(() => {
    async function fetchAndProcessOrder() {
      if (!order.ID || !order.paymentID) throw new Error('Missing required order data');

      await getDeliveryPrice(order);

      order.products.forEach((product) => {
        product.price = preparePrice(product.price);
        product.grossPrice = preparePrice(product.grossPrice);
      });

      const paymentsData = await getPayments(order.ID);
      setPayments(paymentsData);
      setSelectedPayment(
        paymentsData.find((payment) => payment.ID === order.paymentID)
      );
    }

    fetchAndProcessOrder();
  }, [order]);

  return (
    <div>
      {/* Render your component here */}
      {selectedPayment && selectedPayment.name}
      <button onClick={() => setPreventPayment(true)}>Confirm Payment</button>
    </div>
  );
};

export default MyComponent;