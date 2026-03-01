/**
 * Service: CategoriesCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getOne, getDescription, getChilds, getContains } from './services/DpCategoryService';
import { includeTemplateVariables, getTemplateVariable } from './services/MainWidgetService';
import Notification from './utils/Notification';
import _ from 'lodash';

const CategoriesCtrl: React.FC = () => {
    const [category, setCategory] = useState({});
    const dispatch = useDispatch();
    const params = useParams();

    useEffect(() => {
        init();
    }, []);

    const init = async () => {
        let currentCategoryUrl: string;

        ctx.items = [];
        ctx.form = {};
        ctx.groups = [];
        ctx.category = {};
        currentCategoryUrl = params.categoryurl;
        getContains(currentCategoryUrl).then((data) => {
            includeTemplateVariables(ctx, 'group', undefined, undefined, undefined, true);
        });

        const catData = await getOne(currentCategoryUrl);
        setCategory(catData);
        if ($rootScope.currentLang && $rootScope.currentLang.code && catData.langs) {
            $rootScope.customBreadcrumbs.category = catData.langs[$rootScope.currentLang.code].name;
        } else {
            $rootScope.customBreadcrumbs.category = 'category';
        }

        await getDescription(currentCategoryUrl);
    };

    const handleSliderData = (sliderData) => {
        // Handle slider data logic here
    };

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default CategoriesCtrl;