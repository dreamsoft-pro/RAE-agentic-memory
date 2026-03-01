/**
 * Service: footer-in-calc
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const FooterInCalc: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="container-fluid footer-calc-box">
      <div className="row contact-box">
        <div className="col-xs-12">
          <div className="row">
            <div className="contact-left col-xs-6">Kontakt</div>
            <div className="contact-right col-xs-6">
              <div className="social-buttons">
                <span className="fa fa-vk"></span>
                <span className="fa fa-facebook"></span>
                <span className="fa fa-twitter"></span>
                <span className="fa fa-instagram"></span>
                <span className="fa fa-youtube"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="scroll-to-top" onClick={scrollToTop}>
        <i className="fa fa-arrow-circle-o-up"></i>
      </div>
    </div>
  );
};

export default FooterInCalc;