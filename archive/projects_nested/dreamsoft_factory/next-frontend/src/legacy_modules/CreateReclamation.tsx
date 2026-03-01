/**
 * Service: CreateReclamation
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your file `CreateReclamation.tsx`:

/**
 */
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { Notification } from 'react-notification';
import { filter } from 'lodash';
import FileUploader from 'ngx-file-drop';
import MainWidgetService from './services/MainWidgetService';
import ReclamationService from './services/ReclamationService';
import AuthDataService from './services/AuthDataService';
import DpProductService from './services/DpProductService';
import { useTranslation } from 'react-i18next';

const CreateReclamation: React.FC = () => {
    const [faults, setFaults] = useState([]);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [form, setForm] = useState({});
    const [reclamationExist, setReclamationExist] = useState(false);
    const [reclamation, setReclamation] = useState({});
    const [products, setProducts] = useState([]);
    const { orderid } = useParams();
    const { t } = useTranslation();

    const accessTokenName = process.env.REACT_APP_ACCESS_TOKEN_NAME;

    const header = {};
    header[accessTokenName] = AuthDataService.getAccessToken();

    const uploader = new FileUploader({
        headers: header,
        autoUpload: true,
    });

    useEffect(() => {
        uploader.onProgressAll((progress) => setUploadProgress(progress));
    }, [uploader]);

    uploader.filters.push({
        name: 'imageFilter',
        fn: (item) => {
            const itemName = item.name.split('.');
            const lastItem = itemName.pop();
            const possibleExtensions = ['jpg', 'jpeg'];
            if (possibleExtensions.includes(lastItem)) {
                return true;
            } else {
                Notification.warning(t('required_ext') + possibleExtensions.join(','));
                return false;
            }
        },
    });

    const save = () => {
        if (!form.products || form.products.length === 0) {
            Notification.error(t('select_at_least_one_product'));
            return;
        }

        let sum = filter(form.faults, (num) => num === true).length;
        if (sum === 0) {
            Notification.error(t('select_fault_description'));
            return;
        }

        ReclamationService.add(form, orderid).then((data) => {
            if (data.response === true) {
                if (uploader.queue.length > 0) {
                    changeUrl(data.item.ID).then(() => {
                        uploader.uploadAll();
                        uploader.onCompleteAll = () => findReclamation();
                        Notification.success(t('reclamation_created'));
                    });
                } else {
                    findReclamation();
                    Notification.success(t('reclamation_created'));
                }
            }
        });
    };

    const changeUrl = (reclamationID) => {
        return ReclamationService.getUploadUrl(reclamationID).then((urls) => {
            uploader.queue.forEach((item, index) => {
                item.url = urls;
                if (index === uploader.queue.length - 1) {
                    resolve(true);
                }
            });
        });
    };

    const formatSizeUnits = (bytes) => MainWidgetService.formatSizeUnits(bytes);

    const removeFile = (fileItem) => fileItem.remove();

    useEffect(() => {
        ReclamationService.getFaults().then((data) => {
            setForm({ ...form, faults: data.reduce((acc, item) => ({ ...acc, [item.ID]: false }), {}) });
            setFaults(data);
        });
        DpProductService.getByOrder(orderid).then((productData) => setProducts(productData));
    }, []);

    const findReclamation = () => {
        ReclamationService.findByOrder(orderid).then(
            (reclamation) => {
                if (reclamation && reclamation.ID) {
                    setReclamationExist(true);
                    setReclamation(reclamation);
                } else {
                    setReclamationExist(false);
                }
            },
            (error) => {
                setReclamationExist(false);
            }
        );
    };

    return (
        <div>
            <Notification />
            {/* Your component JSX here */}
        </div>
    );
};

export default CreateReclamation;

This modernized version uses React hooks (`useState`, `useEffect`) and TypeScript syntax. It also includes the necessary imports for file uploading, notifications, and translation capabilities. The component is structured to use functional components and hooks instead of a class-based approach found in Angular.