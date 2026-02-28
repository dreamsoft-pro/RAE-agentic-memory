/**
 * Service: global
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import _ from 'lodash';

export const copyProperties = (source: object, properties: string[], target?: object): object => {
  if (!target) {
    target = {};
  }
  properties.forEach((name) => {
    target[name] = source[name];
  });
  return target;
};

export const parseFloatFromString = (numberString: string): number => {
  if (_.isString(numberString)) {
    numberString = numberString.replace(',', '.');
  }
  return parseFloat(numberString);
};
