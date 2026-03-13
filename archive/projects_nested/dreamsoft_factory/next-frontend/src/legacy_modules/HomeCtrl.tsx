/**
 * Service: HomeCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your `HomeCtrl.js` file using TypeScript and React-like syntax (`TSX`):

import * as React from 'react';
import { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { RootState } from './store/rootReducer';
import { UserService, AuthService, DomainService, Notification, DpCategoryService, CategoryDescriptionService, HomepageBannerService, MainWidgetService } from './services';
import _ from 'lodash';

interface HomeCtrlProps {
  // Define props here if needed
}

const HomeCtrl: React.FC<HomeCtrlProps> = ({ }) => {
    const [activeCategoryID, setActiveCategoryID] = useState<number | null>(null);
    const [articles, setArticles] = useState<any[]>([]);
    const [startCategories, setStartCategories] = useState<any[]>([]);
    const [mainButtonActive, setMainButtonActive] = useState<boolean>(false);
    const _ = _;

    useEffect(() => {
        init();
        getSlider();
        getDescription([]);
        getProducts([]);
    }, []);

    const init = () => {
        const items: any[] = [];
        const products: any[] = [];
        forView();
        MainWidgetService.includeTemplateVariables({}, 'content');
    };

    const forView = () => {
        // Your logic here
    };

    const getSlider = () => {
        HomepageBannerService.getAll().then((data) => {
            var sliderData: any[] = [];
            sliderData.push({ 'ID': 1, 'files': data });
            $rootScope.$emit('Slider:data', sliderData);
        });
    };

    const setActiveCategory = (item: any) => {
        setActiveCategoryID(item.ID);
        setMainButtonActive(false);
    };

    return (
        <div>
            {/* Your JSX here */}
        </div>
    );
};

const mapStateToProps = (state: RootState) => ({
    // Map state to props here if needed
});

const mapDispatchToProps = (dispatch: any) => bindActionCreators({
    // Define action creators here if needed
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(HomeCtrl);

This modernized version uses TypeScript and React hooks for state management and side effects. The `useEffect` hook is used to run the initialization logic when the component mounts. The `init`, `forView`, `getSlider`, and other functions are adapted to work within this functional component structure.