/**
 * Service: ngStarRating
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import { PhotoFolderService, Notification } from '@services';
import _ from 'lodash';
import { useTranslation } from 'react-i18next';

const StarRating = ({ ratingValue, max, onRatingSelected, itemId, type }) => {
    const [stars, setStars] = useState({});
    const { t } = useTranslation();

    useEffect(() => {
        initStars();
    }, []);

    const initStars = () => {
        console.log(type);
        const filledRate = Math.round(ratingValue);
        setStars({
            [itemId]: Array.from({ length: max }, (_, i) => ({ filled: i < filledRate }))
        });
    };

    const toggle = (id, index) => {
        if (!isLoggedIn()) {
            Notification.warning(t('login_to_rate'));
            return;
        }
        const newIndex = max - index;
        if (type === 'photo') {
            PhotoFolderService.votePhoto(id, newIndex).then((data) => {
                colorStars(id, data.averageRate);
                updateRate(id, data.averageRate);
            });
        } else if (type === 'folder') {
            PhotoFolderService.voteFolder(id, newIndex).then((data) => {
                colorStars(id, data.averageRate);
                updateRate(id, data.averageRate);
            });
        }
    };

    const colorStars = (id, averageRate) => {
        setStars({
            [id]: Array.from({ length: max }, (_, i) => ({ filled: i < averageRate }))
        });
    };

    const updateRate = (id, rate) => {
        if (type === 'folder') {
            // Assuming you have a way to update the parent state or props
            console.log(scope);
            scope.$parent.folder.averageRate = rate;
        } else if (type === 'photo') {
            const photoIndex = _.findIndex(scope.$parent.photos, { _id: id });
            if (photoIndex > -1) {
                scope.$parent.photos[photoIndex].averageRate = rate;
            }
        }
    };

    const isLoggedIn = () => {
        // Implement your login check logic here
        return $rootScope.logged;
    };

    return (
        <ul className="rating">
            {Array.from({ length: max }, (_, index) => (
                <li key={index} onClick={() => toggle(itemId, index)}>
                    <i className={`fa fa-star ${stars[itemId]?.[index]?.filled ? 'filled' : ''}`} aria-hidden="true"></i>
                </li>
            ))}
        </ul>
    );
};

export default StarRating;