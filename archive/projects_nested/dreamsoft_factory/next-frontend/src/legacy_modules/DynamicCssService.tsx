/**
 * Service: DynamicCssService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { ConfigService } from './config.service'; // Assuming you have a config service for static URL

@Injectable({
  providedIn: 'root'
})
export class DynamicCssService {
  private staticUrl: string;

  constructor(
    @Inject(DOCUMENT) private document: Document,
    private configService: ConfigService
  ) {
    this.staticUrl = this.configService.STATIC_URL || 'http://localtest.me/static/';
  }

  loadDomainCSS(domainID: string, companyID: string): void {
    const cssLink = this.document.createElement('link');

    cssLink.rel = 'stylesheet';
    cssLink.type = 'text/css';
    cssLink.href = `${this.staticUrl}${companyID}/styles/${domainID}/main.css`;

    // Remove any existing domain-specific CSS
    const existingLink = this.document.querySelector('#dynamic-css');
    if (existingLink) {
      existingLink.parentNode.removeChild(existingLink);
    }

    // Set an ID for easier management
    cssLink.id = 'dynamic-css';

    // Append the new CSS file to the head
    this.document.getElementsByTagName('head')[0].appendChild(cssLink);
  }
}
