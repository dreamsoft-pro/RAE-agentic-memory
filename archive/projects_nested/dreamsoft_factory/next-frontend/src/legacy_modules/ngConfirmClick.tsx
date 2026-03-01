/**
 * Service: ngConfirmClick
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import { useRouter } from 'next/router';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

Modal.setAppElement('#__next'); // Ensure modal is accessible

interface NgConfirmClickProps {
    confirmTitle?: string;
    confirmText: string;
    onClick: () => void;
}

const NgConfirmClick: React.FC<NgConfirmClickProps> = ({ confirmTitle, confirmText, onClick }) => {
    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();
    const { t } = useTranslation();

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const handleConfirm = () => {
        onClick();
        closeModal();
    };

    useEffect(() => {
        // Fetch template based on companyID and other conditions if needed
        // Example: axios.get(`${process.env.API_URL}/templates/getFile/35?companyID=${router.query.companyID}`)
        // You can replace this with actual data fetching logic as per your requirements
    }, []);

    return (
        <div>
            <button onClick={openModal}>Trigger Confirmation</button>
            <Modal isOpen={isOpen} onRequestClose={closeModal} contentLabel="Confirm Action">
                <h2>{confirmTitle || t('confirm')}</h2>
                <p>{confirmText ? confirmText : t('irreversible_remove')}</p>
                <button onClick={handleConfirm}>{t('confirm')}</button>
                <button onClick={closeModal}>Cancel</button>
            </Modal>
        </div>
    );
};

export default NgConfirmClick;