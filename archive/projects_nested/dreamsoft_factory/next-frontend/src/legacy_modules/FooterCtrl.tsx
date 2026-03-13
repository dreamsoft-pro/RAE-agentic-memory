/**
 * Service: FooterCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationStart } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NotificationService } from './services/notification.service';
import { SettingService } from './services/setting.service';
import { NewsService } from './services/news.service';
import { TextWidgetService } from './services/text-widget.service';

@Component({
  selector: 'app-footer-ctrl',
  templateUrl: './footer-ctrl.component.html',
  styleUrls: ['./footer-ctrl.component.css']
})
export class FooterCtrl implements OnInit {
  sent = false;
  articles: any[] = [];
  showArticles = false;
  private additionalSettings: any = {};

  constructor(
    private ctx: any,
    private $rootScope: any,
    private $state: any,
    private $filter: any,
    private Notification: NotificationService,
    private Setting: SettingService,
    private NewsService: NewsService,
    private TextWidgetService: TextWidgetService
  ) {}

  sendEmail() {
    this.Setting.setModule('general');
    if (this.newsletterAgreement === undefined || this.newsletterAgreement === false) {
      this.Notification.warning(this.$filter('translate')('subscription_to_newsletter_agreement_info'));
      return false;
    }

    this.Setting.signToNewsletter(this.email).then((data: any) => {
      if (data.response === true) {
        this.sent = true;
        this.Notification.success(this.$filter('translate')(data.info));
      } else {
        this.Notification.error(this.$filter('translate')(data.info));
      }
    });
  }

  ngOnInit() {
    this.$rootScope.$on('$stateChangeStart', (event: any, toState: any, toParams: any, fromState: any, fromParams: any) => {
      if (toState.name === 'home' || toState.name === 'news') {
        if (this.articles.length === 0) {
          this.getNews();
        }
        this.showArticles = true;
      } else {
        this.showArticles = false;
      }
    });

    if ($state.is('home') || $state.is('news')) {
      this.getNews();
      this.showArticles = true;
    } else {
      this.showArticles = false;
    }

    this.Setting.setModule('additionalSettings');
    this.Setting.getPublicSettings().then((data: any) => {
      this.additionalSettings = data;
    });
  }

  private getNews() {
    this.NewsService.getRss().then((data: any) => {
      if (data.items) {
        this.articles = data.items;
      }
    });
  }
}