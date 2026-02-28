/**
 * Service: SearchFormCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from 'react-router-dom';
import Notification from './NotificationService'; // Assuming you have a similar service for notifications

const SearchForm: React.FC = () => {
    const [searchText, setSearchText] = useState('');
    const { t } = useTranslation();
    const history = useHistory();

    const handleSearch = () => {
        if (searchText.length < 3) {
            Notification.warning(t('enter_minimum_chars', { count: 3 }));
            return;
        }
        history.push({ pathname: 'search', search: `text=${encodeURIComponent(searchText)}` });
    };

    return (
        <div>
            <input
                type="text"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder={t('search_placeholder')}
            />
            <button onClick={handleSearch}>{t('search')}</button>
        </div>
    );
};

export default SearchForm;
