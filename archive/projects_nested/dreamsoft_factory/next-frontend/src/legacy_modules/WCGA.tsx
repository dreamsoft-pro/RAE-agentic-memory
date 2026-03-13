/**
 * Service: WCGA
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Directive, ElementRef } from '@angular/core';
import { LocalStorageService, SettingService } from 'path-to-services'; // Adjust the import paths accordingly

@Directive({
  selector: 'wcga',
  providers: [LocalStorageService, SettingService]
})
export class WcgaDirective {
  private wcgaUsed: boolean;

  constructor(private el: ElementRef, private localStorageService: LocalStorageService, private settingService: SettingService) {
    const Setting = new settingService('additionalSettings');
    Setting.getPublicSettings().then((settingsData) => {
      this.wcgaUsed = settingsData.wcgaUsed.value;
      if (this.wcgaUsed) {
        this.applyContrast();
        this.applyFontSize();
      }
    });
  }

  changeContrast() {
    this.el.nativeElement.classList.toggle('wcga-contrast');
    if (this.el.nativeElement.classList.contains('wcga-contrast')) {
      this.localStorageService.set('wcgaKontrast', 1);
    } else {
      this.localStorageService.remove('wcgaKontrast');
    }
  }

  toggleFontSize() {
    this.el.nativeElement.classList.toggle('wcga-fonts');
    if (this.el.nativeElement.classList.contains('wcga-fonts')) {
      this.localStorageService.set('wcgaFonts', 1);
    } else {
      this.localStorageService.remove('wcgaFonts');
    }
  }

  private applyContrast() {
    if (this.localStorageService.keys().indexOf('wcgaKontrast') > -1) {
      this.el.nativeElement.classList.add('wcga-contrast');
    }
  }

  private applyFontSize() {
    if (this.localStorageService.keys().indexOf('wcgaFonts') > -1) {
      this.el.nativeElement.classList.add('wcga-fonts');
    }
  }
}