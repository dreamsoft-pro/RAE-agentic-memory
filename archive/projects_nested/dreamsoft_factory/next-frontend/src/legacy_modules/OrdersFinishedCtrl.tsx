/**
 * Service: OrdersFinishedCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as React from 'react';
import { useState, useEffect } from 'react';
import { observer } from 'mobx-react';
import { inject, observer } from 'mobx-react';
import { Modal, Button } from 'react-bootstrap';
import _ from 'lodash';
import axios from 'axios';

interface OrdersFinishedCtrlProps {
    // Define props here if needed
}

const OrdersFinishedCtrl: React.FC<OrdersFinishedCtrlProps> = ({ 
    ctx, 
    $rootScope, 
    DeliveryWidgetService, 
    $config, 
    $modal, 
    ClientZoneWidgetService, 
    FileUploader, 
    ProductFileService, 
    AuthDataService, 
    $filter, 
    Notification, 
    TemplateRootService, 
    InvoiceService, 
    MainWidgetService, 
    DpProductService, 
    CommonService 
}) => {
    const [isCollapsed, setIsCollapsed] = useState(true);
    const [statuses, setStatuses] = useState([]);
    const [deliveries, setDeliveries] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [senders, setSenders] = useState([]);
    const [orders, setOrders] = useState([]);
    const [firstStatus, setFirstStatus] = useState({});
    const [pagingSettings, setPagingSettings] = useState({});
    const [pageSizeSelect, setPageSizeSelect] = useState({});

    useEffect(() => {
        // Fetch data if needed on component mount or update
        setPagingSettings(ClientZoneWidgetService.getPagingSettings());
        setPageSizeSelect(ClientZoneWidgetService.getPageSizeSelect());
    }, []);

    const accessTokenName = $config.ACCESS_TOKEN_NAME;

    const handleUploadFiles = (product) => {
        TemplateRootService.getTemplateUrl(34).then((response) => {
            $modal.open({
                templateUrl: response.url,
                scope: ctx,
                backdrop: true,
                keyboard: false,
                size: 'lg',
                resolve: {
                    allowedExtensions: () => CommonService.getAll().then((data) => {
                        const extensions = [];
                        _.each(data, (item) => {
                            extensions.push(item['extension']);
                        });
                        return extensions;
                    })
                },
                controller: (ctx, $modalInstance, allowedExtensions) => {
                    let header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();
                }
            });
        });
    };

    const handlePaymentConfirm = (paymentID) => {
        ClientZoneWidgetService.payment({ paymentID: paymentID }, order.ID).then((paymentResponse) => {
            if (_.isEmpty(paymentResponse.payment)) {
                setPreventPayment(false);
            }
        });
    };

    const handleDeleteProduct = (order, product) => {
        DpProductService.delete(product).then((data) => {
            if (data.response === true) {
                const idx = _.findIndex(order.products, { ID: product.ID });
                if (idx > -1) {
                    Notification.success($filter('translate')('deleted_successful'));
                    order.products.splice(idx, 1);
                }
            } else {
                Notification.error($filter('translate')('error'));
            }
        });
    };

    const handleRestoreAccept = (product) => {
        const newFiles = product.fileList.filter((obj) => 0 === parseInt(obj.accept));

        if (newFiles.length === 0) {
            Notification.warning($filter('translate')('should_upload_corrected_files'));
            return;
        }

        DpProductService.restoreAccept(product.productID).then((data) => {
            if (data.response === true) {
                product.fileList = product.fileList.filter((obj) => -1 !== parseInt(obj.accept));
            }
        });
    };

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default inject('store')(observer(OrdersFinishedCtrl));