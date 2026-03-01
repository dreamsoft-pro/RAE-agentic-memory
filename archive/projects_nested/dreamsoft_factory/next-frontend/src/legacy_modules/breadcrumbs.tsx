/**
 * Service: breadcrumbs
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Step {
  name: string;
  ncyBreadcrumbLabel?: string;
  ncyBreadcrumbLink?: string;
  abstract?: boolean;
}

interface Props {
  steps: Step[];
  customBreadcrumbs: Record<string, string>;
}

const Breadcrumbs: React.FC<Props> = ({ steps, customBreadcrumbs }) => {
  return (
    <ol className="breadcrumb">
      {steps.map((step, index) => (
        <li key={index} className={$last ? 'active' : ''}>
          {step.ncyBreadcrumbLink ? (
            <a href={step.ncyBreadcrumbLink}>
              {(!customBreadcrumbs[step.name] || customBreadcrumbs[step.name] !== step.name) && step.ncyBreadcrumbLabel ? (
                <span>{step.ncyBreadcrumbLabel}</span>
              ) : (
                <span>{customBreadcrumbs[step.name]}</span>
              )}
            </a>
          ) : (
            <>
              {(!customBreadcrumbs[step.name] || customBreadcrumbs[step.name] !== step.name) && step.ncyBreadcrumbLabel ? (
                <span>{step.ncyBreadcrumbLabel}</span>
              ) : (
                <span>{customBreadcrumbs[step.name]}</span>
              )}
            </>
          )}
        </li>
      ))}
    </ol>
  );
};

export default Breadcrumbs;