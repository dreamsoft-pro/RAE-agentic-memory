/**
 * Service: TemplateRootService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next-core';
import axios from 'axios';

@Injectable()
export class TemplateRootService {
  private resource = 'templates';

  constructor(private $config: Config) {}

  public getTemplateUrl(templateID: string): Promise<any> {
    const url = `${this.$config.API_URL}/${this.resource}/getUrl/${templateID}`;
    return axios.get(url).then(response => response.data);
  }
}
