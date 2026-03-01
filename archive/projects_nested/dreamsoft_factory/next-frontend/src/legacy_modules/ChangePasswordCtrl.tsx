/**
 * Service: ChangePasswordCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Notification from './Notification'; // Assuming you have a similar component for notifications
import UserService from './UserService'; // Adjust the import according to your project structure

const ChangePasswordCtrl: React.FC = () => {
    const { t } = useTranslation();
    const [form, setForm] = useState({ pass: '', confirmPass: '' });
    const [errorNotification, setErrorNotification] = useState('');
    const [successNotification, setSuccessNotification] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    };

    const validatePasswords = () => {
        return form.pass === form.confirmPass;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!validatePasswords()) {
            setErrorNotification(t('passwords_not_same'));
            return;
        }

        try {
            const data = await UserService.changePass(form);
            if (data.response === true) {
                setSuccessNotification(t('successfully_edited'));
            } else {
                setErrorNotification(t('error'));
            }
        } catch (err) {
            setErrorNotification(t('error'));
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="password" name="pass" value={form.pass} onChange={handleChange} placeholder={t('new_password')} />
            <input type="password" name="confirmPass" value={form.confirmPass} onChange={handleChange} placeholder={t('confirm_password')} />
            <button type="submit">{t('change_password')}</button>
            {errorNotification && <Notification type="error">{errorNotification}</Notification>}
            {successNotification && <Notification type="success">{successNotification}</Notification>}
        </form>
    );
};

export default ChangePasswordCtrl;

