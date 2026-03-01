/**
 * Service: LangLoader
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { injectable } from 'inversify';
import { LangService } from './langService'; // Assuming you have a LangService module

@injectable()
export class LangLoader {
  private langService: LangService;

  constructor(langService: LangService) {
    this.langService = langService;
  }

  public getLang(options: { key?: string }) {
    const selectedLang = options.key ?? 'pl';
    return this.langService.getLang(selectedLang);
  }
}
