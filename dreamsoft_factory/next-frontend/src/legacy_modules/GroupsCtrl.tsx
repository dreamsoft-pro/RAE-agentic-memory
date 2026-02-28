/**
 * Service: GroupsCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getTypes, getGroup, getOne, getDescription } from './actions'; // Assuming you have corresponding actions defined
import { filter, q } from 'lodash'; // Importing lodash functions as needed
import Notification from './NotificationService'; // Adjust the import based on your file structure
import MainWidgetService from './MainWidgetService'; // Similarly adjust this import

const GroupsCtrl: React.FC = () => {
    const [items, setItems] = useState<any[]>([]);
    const [galleries, setGalleries] = useState<any[]>([]);
    const [descriptions, setDescriptions] = useState<any[]>([]);
    const [group, setGroup] = useState<any>({});
    const [category, setCategory] = useState<any>({});
    const [form, setForm] = useState<any>({});

    const { groupurl } = useParams();
    const location = useLocation();
    const dispatch = useDispatch();

    useEffect(() => {
        init();
    }, []);

    const init = () => {
        setItems([]);
        setGroup({});
        setCategory({});
        setForm({});
        getTypes(groupurl);
        getGroup(groupurl);
        getOne(location.categoryurl);
        getDescription(groupurl);
    };

    const getTypes = (currentGroupUrl: string) => {
        // Dispatch an action or perform the API call here
    };

    const getGroup = (currentGroupUrl: string) => {
        PsGroupService.getOneForView(currentGroupUrl).then((data) => {
            setGroup(data);
            if ($rootScope.currentLang && $rootScope.currentLang.code) {
                $rootScope.customBreadcrumbs.group = data.names[$rootScope.currentLang.code];
            } else {
                $rootScope.customBreadcrumbs.group = $filter('translate')('group');
            }
            MainWidgetService.includeTemplateVariables(data.ID);
        }, (error) => {
            Notification.error($filter('translate')('error'));
        });
    };

    const getOne = (currentCategoryUrl: string) => {
        DpCategoryService.getOneForView(currentCategoryUrl).then((data) => {
            setCategory(data);
            if ($rootScope.currentLang && $rootScope.currentLang.code && data.langs) {
                $rootScope.customBreadcrumbs.category = data.langs[$rootScope.currentLang.code].name;
            } else {
                $rootScope.customBreadcrumbs.category = $filter('translate')('category');
            }
        }, (error) => {
            Notification.error($filter('translate')('error'));
        });
    };

    const getDescription = (groupUrl: string) => {
        PsGroupDescriptionService.getAll(groupUrl).then((data) => {
            let sliderData = [];
            if (!_.isEmpty(data)) {
                _.each(data, (oneDesc) => {
                    switch (oneDesc.descType) {
                        case 1:
                            setDescriptions(prev => [...prev, oneDesc]);
                            break;
                        case 5:
                            oneDesc.items = [];
                            if (!_.isEmpty(oneDesc.files)) {
                                _.each(oneDesc.files, (oneFile) => {
                                    oneDesc.items.push({
                                        thumb: oneFile.urlCrop,
                                        img: oneFile.url,
                                        description: 'Image ' + oneFile.fileID
                                    });
                                });
                            }
                            setGalleries(prev => [...prev, oneDesc]);
                    }
                });
            } else if ((ctx.attributeDescView == 0 || ctx.attributeDescView == 3) && ctx.attributeMenuLeft == 0 && ctx.attributeIconsCount == 1) {
                return 'col-xs-12 col-sm-4 col-md-2 col-lg-2 col-md-' + (iconWidth * 2) + '-20pp';
            } else if ((ctx.attributeDescView == 0 || ctx.attributeDescView == 3) && ctx.attributeMenuLeft == 0 && ctx.attributeIconsCount == 2) {
                return 'col-xs-6 col-sm-3 col-md-' + (iconWidth * 2) + ' col-lg-' + (iconWidth * 2);
            } else if ((ctx.attributeDescView == 1 || ctx.attributeDescView == 2) && ctx.attributeMenuLeft == 0) {
                return 'col-xs-12 col-sm-12 col-md-6 col-lg-6';
            } else if (ctx.attributeMenuLeft == 1) {
                // Handle other cases
            }
        }, (error) => {
            Notification.error($filter('translate')('error'));
        });
    };

    return <div>GroupsCtrl Component</div>;
};

export default GroupsCtrl;