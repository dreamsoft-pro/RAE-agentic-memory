/**
 * Service: DeliveryDataCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Component } from '@angular/core';
import { ModalController } from 'ngx-modal'; // Assuming you're using ngx-modal for modal management
import { DpAddressService } from './services/dpAddress.service';
import { CountriesService } from './services/countries.service';
import { NotificationService } from './services/notification.service';
import { FilterService } from './services/filter.service';
import { ConfigService } from './services/config.service';
import { TemplateRootService } from './services/templateRoot.service';
import { RegisterWidget } from './registerWidget';

@Component({
  selector: 'app-delivery-data',
  templateUrl: './deliveryDataCtrl.component.html'
})
export class DeliveryDataCtrl {
  countries: any[] = [];
  addresses: any[] = [];
  form: any = {};

  constructor(
    private ctx: any,
    private $rootScope: any,
    private DpAddressService: DpAddressService,
    private CountriesService: CountriesService,
    private Notification: NotificationService,
    private $filter: FilterService,
    private $config: ConfigService,
    private $modal: ModalController,
    private TemplateRootService: TemplateRootService,
    private RegisterWidget: RegisterWidget
  ) {
    this.init();
  }

  async init() {
    await this.getAddresses();
    await this.CountriesService.getAll().then((dataCountries) => {
      this.countries = dataCountries;
    });
  }

  async getAddresses() {
    const data = await this.DpAddressService.getAddresses(1);
    this.addresses = data;
  }

  addressEdit(address: any) {
    this.TemplateRootService.getTemplateUrl(65).then((response) => {
      this.$modal.open({
        templateUrl: response.url,
        scope: this.ctx,
        size: 'lg',
        controller: (ctx: any, $modalInstance: any) => {
          ctx.modalForm = address;

          ctx.save = async () => {
            const data = await this.DpAddressService.editUserAddress(ctx.modalForm, ctx.modalForm.ID);
            if (data.response === true) {
              // Handle success
            } else {
              // Handle error
            }
          };

          ctx.cancel = () => {
            $modalInstance.close();
          };
        }
      });
    });
  }

  addressRemove(address: any) {
    this.DpAddressService.remove(address.ID).then((removedData) => {
      if (removedData.response) {
        const idx = _.findIndex(this.addresses, { ID: address.ID });
        if (idx > -1) {
          this.addresses.splice(idx, 1);
        }
        this.Notification.success(this.$filter('translate')('deleted_successful'));
      } else {
        this.Notification.error(this.$filter('translate')('error'));
      }
    }, () => {
      this.Notification.error(this.$filter('translate')('error'));
    });
  }

  async add() {
    const data = await this.DpAddressService.addAddress(this.form, 1);
    if (data.response === true) {
      this.addresses.push(data.item);
      this.form = {};
      this.Notification.success(this.$filter('translate')('added'));
    } else {
      this.Notification.error(this.$filter('translate')('error'));
    }
  }

  isCountryCode(formName: string): boolean {
    const country = _.find(this.countries, { code: this.ctx[formName].countryCode });
    return country && String(country.areaCode).length > 0;
  }

  updateAreaCode(formName: string) {
    const country = _.find(this.countries, { code: this.ctx[formName].countryCode });
    this.ctx[formName].areaCode = country.areaCode;
  }
}