/**
 * Service: config
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Provider, Injector } from 'angular';

export class ConfigProvider implements Provider<any> {
  private static config = {};

  public set(key: string, val: any): void {
    ConfigProvider.config[key] = val;
  }

  public get(key: string): any {
    return ConfigProvider.config[key];
  }

  public $get(): any {
    return ConfigProvider.config;
  }
}

export const configModule = angular.module('dpClient.config', [])
  .provider('$config', () => new ConfigProvider());
