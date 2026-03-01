/**
 * Service: OrdersCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your `OrdersCtrl.js` file using TypeScript and React-like syntax (TSX):

import * as React from 'react';
import { useState, useEffect } from 'react';
import { observer } from 'mobx-react';
import { Modal, Button } from 'react-bootstrap';
import { 
    DeliveryWidgetService, 
    ClientZoneWidgetService, 
    FileUploader, 
    ProductFileService, 
    AuthDataService, 
    Notification, 
    TemplateRootService, 
    InvoiceService, 
    MainWidgetService, 
    DpProductService, 
    CommonService, 
    CartWidgetService 
} from './services';
import { useTranslation } from 'react-i18next';

const OrdersCtrl: React.FC = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [statuses, setStatuses] = useState<any[]>([]);
    const [deliveries, setDeliveries] = useState<any[]>([]);
    const [addresses, setAddresses] = useState<any[]>([]);
    const [senders, setSenders] = useState<any[]>([]);
    const [orders, setOrders] = useState<any[]>([]);
    const [firstStatus, setFirstStatus] = useState<any>({});
    const [orderFilters, setOrderFilters] = useState<{ dateFrom: Date | null; dateTo: Date | null; text: string | null }>({ dateFrom: null, dateTo: null, text: null });
    const [pageSizeSelect, setPageSizeSelect] = useState<any>(ClientZoneWidgetService.getPageSizeSelect());
    const [pagingSettings, setPagingSettings] = useState<any>(ClientZoneWidgetService.getPagingSettings());

    useEffect(() => {
        init();
    }, []);

    const init = () => {
        ClientZoneWidgetService.getStatuses().then((statuses) => {
            setStatuses(statuses);
            setFirstStatus(_.find(statuses, { type: 1 }));
            ClientZoneWidgetService.clearParams();
            ClientZoneWidgetService.addParam('statusTypeList', [0, 1].join(','));
            ClientZoneWidgetService.mergeFiles(ordersData);
            setOrders(ordersData);
        });
    };

    const showDelivery = (order: any, product: any) => {
        TemplateRootService.getTemplateUrl(104).then((response) => {
            Modal.open({
                title: 'Delivery Details',
                content: response.url,
                size: 'lg',
                onCancel: () => {},
                onOk: () => {}
            });
        });
    };

    const deleteProduct = (order: any, product: any) => {
        DpProductService.delete(product).then((data) => {
            if (data.response === true) {
                const idx = _.findIndex(order.products, { ID: product.ID });
                if (idx > -1) {
                    Notification.success('Product deleted successfully');
                    order.products.splice(idx, 1);
                }
            } else {
                Notification.error('Error occurred while deleting the product');
            }
        });
    };

    const restoreAccept = (product: any) => {
        const newFiles = product.fileList.filter((obj: any) => 0 === parseInt(obj.accept));
        if (newFiles.length === 0) {
            Notification.warning('You should upload corrected files');
            return;
        }
        DpProductService.restoreAccept(product.productID).then((data) => {
            if (data.response === true) {
                product.fileList = product.fileList.filter((obj: any) => -1 !== parseInt(obj.accept));
                setAccept(0);
                Notification.success('Files restored successfully');
            } else {
                Notification.error('Error occurred while restoring the files');
            }
        });
    };

    return (
        <div>
            {/* Your component JSX here */}
        </div>
    );
};

export default observer(OrdersCtrl);

This modernized version uses TypeScript and React hooks for state management, making the code more readable and maintainable. It also includes some placeholder functions and logic that you would need to complete based on your specific requirements.