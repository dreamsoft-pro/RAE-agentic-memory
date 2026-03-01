/**
 * Service: description-accordion
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { Accordion, AccordionGroup, AccordionHeading } from '@material-ui/core'; // Assuming Material-UI for similar components
import parseHtmlString from './utils/parseHtmlString'; // Custom utility to handle HTML strings
import { useTranslation } from 'react-i18next'; // Hook for internationalization

interface Description {
  langs: { [key: string]: { name: string; description: string } };
  showLess: boolean;
  initHide: boolean;
}

interface Props {
  descriptions: Description[];
  currentLang: { code: string };
}

const DescriptionAccordion: React.FC<Props> = ({ descriptions, currentLang }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const { t } = useTranslation();

  return (
    <Accordion>
      {descriptions.map((description, index) => (
        <AccordionGroup key={index} expanded={openIndex === index}>
          <AccordionHeading onClick={() => setOpenIndex(openIndex === index ? null : index)}>
            {description.langs[currentLang.code].name}
            <i className="pull-right fa">
              {openIndex === index ? 'fa-chevron-down' : 'fa-chevron-right'}
            </i>
          </AccordionHeading>
          {description.showLess && (
            <div>
              <div hidden={!description.initHide} dangerouslySetInnerHTML={{ __html: description.showLess }} />
              <div hidden={description.initHide} dangerouslySetInnerHTML={{ __html: description.langs[currentLang.code].description }} />
              <div className="pull-right">
                <button onClick={() => (description.initHide = false)}>
                  {t('expand')} <i className="fa fa-chevron-down"></i>
                </button>
                <button onClick={() => (description.initHide = true)}>
                  {t('collapse')} <i className="fa fa-chevron-up"></i>
                </button>
              </div>
            </div>
          )}
          {!description.showLess && (
            <div dangerouslySetInnerHTML={{ __html: description.langs[currentLang.code].description }} />
          )}
        </AccordionGroup>
      ))}
    </Accordion>
  );
};

export default DescriptionAccordion;