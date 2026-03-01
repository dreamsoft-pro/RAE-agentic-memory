import { $q } from './httpBridge';
/**
 * Service: CustomProductCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { FileUploader } from 'ngx-file-drop';
import _ from 'lodash';
import { Notification } from 'angular-notification-service'; // Assuming this is a service for notifications
import { SettingService, PsTypeDescriptionService, PsTypeService, DpCategoryService, PsGroupService } from './services'; // Adjust the import paths as necessary

const CustomProductCtrl: React.FC = () => {
    const [formSent, setFormSent] = useState(false);
    const [customProduct, setCustomProduct] = useState(false);
    const [descriptions, setDescriptions] = useState<any[]>([]);
    const [galleries, setGalleries] = useState<any[]>([]);
    const [thumbnails, setThumbnails] = useState<any[]>([]);
    const [patterns, setPatterns] = useState<any[]>([]);
    const [uploadProgress, setUploadProgress] = useState(0);
    const { groupurl, typeurl } = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const accessTokenName = useSelector((state: any) => state.config.ACCESS_TOKEN_NAME);

    const header = {};
    if (accessTokenName) {
        header[accessTokenName] = AuthDataService.getAccessToken();
    }

    const uploader = new FileUploader({ headers: header, autoUpload: true });

    useEffect(() => {
        init();
    }, []);

    const init = () => {
        getType(groupurl, typeurl).then((responseData) => {
            getDescriptions();
            if (!groupurl) {
                getGroup(responseData.group.slugs[currentLang.code]);
            } else {
                getGroup(groupurl);
            }
            if (!state.params.categoryurl) {
                getCategory(responseData.category.langs[currentLang.code].url);
            } else {
                getCategory(state.params.categoryurl);
            }
        });
    };

    const getType = (groupUrl: string, typeUrl: string) => {
        const def = $q.defer();
        PsTypeService.getOneForView(groupUrl, typeUrl).then((data) => {
            if (data && data.active === 0) {
                Notification.error($filter('translate')('product_currently_not_available'));
                navigate('home');
                return;
            }
            currentGroupID = data.groupID;
            currentTypeID = data.ID;
            def.resolve(data);
        }, (data) => {
            console.error(data);
            Notification.error($filter('translate')('error'));
            def.reject(data);
        });
        return def.promise;
    };

    const getDescriptions = () => {
        // Assuming this function fetches descriptions and updates the state
    };

    const getGroup = (currentGroupUrl: string) => {
        PsGroupService.getOneForView(currentGroupUrl).then((data) => {
            if ($rootScope.currentLang && $rootScope.currentLang.code) {
                customBreadcrumbs.group = data.names[$rootScope.currentLang.code];
            } else {
                customBreadcrumbs.group = $filter('translate')('group');
            }
        }, (data) => {
            Notification.error($filter('translate')('error'));
        });
    };

    const getCategory = (currentCategoryUrl: string) => {
        DpCategoryService.getOneForView(currentCategoryUrl).then((data) => {
            category = data;
            if ($rootScope.currentLang && $rootScope.currentLang.code && data.langs) {
                customBreadcrumbs.category = data.langs[$rootScope.currentLang.code].name;
            } else {
                customBreadcrumbs.category = $filter('translate')('category');
            }
        });
    };

    const formatSizeUnits = (bytes: number) => {
        return MainWidgetService.formatSizeUnits(bytes);
    };

    const removeFile = (fileItem: any) => {
        fileItem.remove();
    };

    const hasFormats = (desc: any) => {
        return true;
    };

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default CustomProductCtrl;