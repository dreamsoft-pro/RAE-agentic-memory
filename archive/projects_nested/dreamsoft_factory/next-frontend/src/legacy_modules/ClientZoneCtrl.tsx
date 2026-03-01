/**
 * Service: ClientZoneCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as _ from 'lodash';
import { Component, OnInit } from '@angular/core';
import { StateService } from '@uirouter/angular';
import { NotificationService, FilterService } from 'angular-notification-service'; // Assuming you have a notification service

@Component({
  selector: 'app-client-zone-ctrl',
  templateUrl: './client-zone-ctrl.component.html'
})
export class ClientZoneCtrl implements OnInit {
  public menuTop: any[] = [];
  public menuBottom: any[] = [];
  public currentState: string = '';
  public searchType: string = 'simple';
  public showQuota: boolean = false;
  public usedSpace: number = 0;

  constructor(private ctx: ng.IScope, private $state: StateService, private $rootScope: any, private Notification: NotificationService, private $filter: FilterService) {}

  public ngOnInit(): void {
    this.init();
  }

  private init(): void {
    this.currentState = this.$state.current.name;

    const topMenuList = [
      this.$state.get('client-zone-orders'),
      this.$state.get('client-zone-orders-not-paid'),
      this.$state.get('client-zone-orders-finished'),
      this.$state.get('client-zone-offers'),
      this.$state.get('client-zone-questions'),
      this.$state.get('client-zone-reclamations'),
      this.$state.get('client-zone-my-folders'),
      this.$state.get('client-zone-my-projects')
    ];

    _.each(topMenuList, (element) => {
      if (element !== null) {
        this.menuTop.push(element);
      }
    });

    const bottomMenuList = [
      this.$state.get('client-zone-data'),
      this.$state.get('client-zone-delivery-data'),
      this.$state.get('client-zone-invoice-data'),
      this.$state.get('client-zone-change-pass')
    ];

    _.each(bottomMenuList, (element) => {
      if (element !== null) {
        this.menuBottom.push(element);
      }
    });

    if ($rootScope.companyID === 195 || $rootScope.companyID === 35) {
      this.usedSpace = ((parseInt($rootScope.user.userID) * 1234) % 1000);
      this.showQuota = true;
    }
  }

  public changeSearchType(type: string): void {
    this.searchType = type;
  }

  public search(): void {
    if ($rootScope.companyID === 195 || $rootScope.companyID === 35 || $rootScope.companyID === 25) {
      if (this.searchType === 'simple' && (this.tag === undefined || this.tag.length < 3)) {
        this.Notification.warning(this.$filter('translate')('input_min_3_characters'));
        return;
      }

      if (this.tag !== undefined) {
        this.$state.go('client-zone-search', { q: this.tag, subject: 'tag' });
      } else if (this.author !== undefined) {
        this.$state.go('client-zone-search', { q: this.author, subject: 'author' });
      } else if (this.place !== undefined) {
        console.log(this.place);
        this.$state.go('client-zone-search', { q: this.place, subject: 'place' });
      } else if (this.person !== undefined) {
        this.$state.go('client-zone-search', { q: this.person, subject: 'person' });
      } else if (this.minRating !== undefined && this.maxRating !== undefined) {
        this.$state.go('client-zone-search', { q: `${this.minRating}-${this.maxRating}`, subject: 'rating' });
      }
    }
  }
}