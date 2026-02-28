import { NextApiRequest, NextApiResponse } from 'next';
import api from '@/lib/api';
import { Notification } from '@/components/Notification'; // Adjust import based on actual location of Notification component

interface PaymentResponse {
  response: boolean;
  paid?: boolean;
  payment?: {
    status: string;
    statusCode?: string;
    redirectUri?: string;
    url?: string;
    formUrl?: string;
    operator?: string;
    info?: string;
  };
  paymentChanged?: boolean;
  paymentInfo?: string;
}

interface Order {
  paid: number | boolean;
  paymentID?: string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { paymentResponse, order, payments } = req.body as {
    paymentResponse: PaymentResponse;
    order: Order;
    payments: Array<{ ID: string }>;
  };

  if (paymentResponse.response === false && paymentResponse.paid === true) {
    order.paid = 1;
    Notification.info('order_already_paid');
    res.json({ redirect: null });
  } else if (paymentResponse.response === true && paymentResponse.payment !== undefined) {
    const { status, statusCode, redirectUri, url, formUrl, operator, info } = paymentResponse.payment;

    if (statusCode === "SUCCESS") {
      res.json({ redirect: redirectUri });
    }

    if (status === 'NEW' && operator === 'tinkoff') {
      res.json({ redirect: url });
    }

    if (status === 'NEW' && operator === 'sberbank') {
      res.json({ redirect: formUrl });
    }

    if (status === 'CREATED' && operator === 'sberbank') {
      Notification.info(info);
      res.json({ redirect: null });
    }
  } else if (paymentResponse.response === true && paymentResponse.paymentChanged === true) {
    Notification.info('payment_method_changed');
    order.paymentID = req.body.paymentID;
    const selectedPayment = payments.find(payment => payment.ID === order.paymentID);
    res.json({ selectedPayment });
  } else if (paymentResponse.response === false) {
    Notification.error(info ?? 'unknown_error'); // Adjust based on actual error message structure
    res.status(500).json({ error: info ?? 'unknown_error' });
  }
}