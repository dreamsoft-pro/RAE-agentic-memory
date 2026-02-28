/**
 * Service: footer-in-cart
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const FooterInCart: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div>
      <div data-include="views/partial/showThumbnail.html"></div>
      <div data-cookie-information></div>
      <div className="scroll-to-top" onClick={scrollToTop}>
        <i className="fa fa-arrow-circle-o-up"></i>
      </div>
      <div className="footer-gap"></div>
    </div>
  );
};

export default FooterInCart;