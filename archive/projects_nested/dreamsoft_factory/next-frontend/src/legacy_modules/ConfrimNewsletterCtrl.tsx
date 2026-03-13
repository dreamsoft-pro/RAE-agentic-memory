/**
 * Service: ConfrimNewsletterCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Notification from '@components/Notification'; // Assuming you have a Notification component
import SettingService from '@services/SettingService'; // Assuming you have a SettingService

const ConfirmNewsletter: React.FC = () => {
    const router = useRouter();
    const [confirmation, setConfirmation] = useState({ success: '', error: '' });

    useEffect(() => {
        if (router.isReady) {
            const token = router.query.token as string;
            const settingService = new SettingService('general');

            const confirmNewsletter = async () => {
                try {
                    const data = await settingService.confirmNewsletter(token);
                    if (data.response === true) {
                        setConfirmation({ ...confirmation, success: data.info });
                    } else {
                        setConfirmation({ ...confirmation, error: data.info });
                    }
                } catch (error) {
                    console.error('Error confirming newsletter:', error);
                }
            };

            confirmNewsletter();
        }
    }, [router.isReady, router.query.token]);

    return (
        <div>
            {confirmation.success && <Notification type="success">{confirmation.success}</Notification>}
            {confirmation.error && <Notification type="error">{confirmation.error}</Notification>}
        </div>
    );
};

export default ConfirmNewsletter;

