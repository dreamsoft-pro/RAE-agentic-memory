/**
 * Service: ContactFormCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import { Component } from 'react';
import { RouteComponentProps } from 'react-router-dom';
import { ctx, $state, $filter, Notification, SettingService, vcRecaptchaService } from './dependencies';

interface ContactFormModel {
    key: string;
}

@ctx('ContactFormCtrl')
class ContactFormCtrl extends Component<RouteComponentProps> {
    public ctx: any;
    public $state: any;
    public $filter: any;
    public Notification: any;
    public SettingService: any;
    public vcRecaptchaService: any;

    public model: ContactFormModel = { key: '' };
    public response: string | null = null;
    public widgetId: string | null = null;
    public mailSent: boolean = false;

    constructor(props: RouteComponentProps) {
        super(props);
        this.ctx = props.ctx;
        this.$state = props.$state;
        this.$filter = props.$filter;
        this.Notification = props.Notification;
        this.SettingService = props.SettingService;
        this.vcRecaptchaService = props.vcRecaptchaService;
    }

    public setResponse(response: string) {
        console.info('Response available');
        this.response = response;
    }

    public setWidgetId(widgetId: string) {
        console.info('Created widget ID: %s', widgetId);
        this.widgetId = widgetId;
    }

    public cbExpiration() {
        console.info('Captcha expired. Resetting response object');
        this.vcRecaptchaService.reload(this.widgetId);
        this.response = null;
    }

    public sendMessage(key: string) {
        console.log('sending the captcha response to the server', this.response);

        const contactData = ctx.contactForm;
        contactData.captchaResponse = this.response;

        const Setting = new this.SettingService('forms');

        Setting.sendMessage(key, contactData).then((sentData: any) => {
            if (sentData.response === true) {
                this.Notification.success(this.$filter('translate')('email_sended'));
                this.mailSent = true;
            } else {
                this.Notification.error(this.$filter('translate')('error'));
            }
        }, (errorData: any) => {
            if (errorData.info) {
                this.Notification.error(this.$filter('translate')(errorData.info));
            } else {
                this.Notification.error(this.$filter('translate')('error'));
            }
        });
    }

    public componentDidMount() {
        const Setting = new this.SettingService('additionalSettings');
        Setting.getPublicSettings().then((settingsData: any) => {
            if (settingsData.captchaPublicKey) {
                this.model = { key: settingsData.captchaPublicKey.value };
            }
        });
    }
}

export default ContactFormCtrl;