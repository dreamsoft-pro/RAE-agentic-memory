import api from '@/lib/api';
import { useState, useEffect } from 'react';

const PaymentComponent = ({ payments, paymentID, order }) => {
    const [preventPayment, setPreventPayment] = useState(true);

    useEffect(() => {
        const handlePaymentCheck = async () => {
            const paymentIdx = payments.findIndex(payment => payment.ID === paymentID);
            
            if (paymentIdx > -1) {
                const paymentType = payments[paymentIdx];
                
                if (paymentType.limitExceeded) {
                    setPreventPayment(false);
                    alert(`Credit limit exceeded - ${paymentType.creditLimit}/${paymentType.unpaidValue} ${paymentType.baseCurrency}`);
                    return;
                }
            }

            try {
                const paymentResponse = await api.payment({ paymentID, orderID: order.ID });
                
                if (Object.keys(paymentResponse.payment).length === 0) {
                    setPreventPayment(false);
                }
            } catch (error) {
                console.error('Error processing payment:', error);
            }
        };

        handlePaymentCheck();
    }, [payments, paymentID, order]);

    return (
        <div>
            {/* Your component JSX here */}
        </div>
    );
};

export default PaymentComponent;