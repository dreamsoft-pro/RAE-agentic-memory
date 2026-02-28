/**
 * Service: ngCookieInformation
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const CookieInformation: React.FC = () => {
  const setupKlaro = () => {
    if (typeof window !== 'undefined') {
      const klaro = window.klaro;
      klaro.setup({
        languages: ['pl', 'en', 'ge', 'ru'],
        cookieExpiresAfterDays: 30,
        hideDeclineAll: true,
        services: [
          {
            name: 'Google tag manager',
            required: true,
            purposes: ['analytics'],
            cookies: [/^(?!_gtm(_.*)?/],
            onAccept: "for(var k of Object.keys(opts.consents)){if(opts.consents[k]){var eventName='klaro-'+k+'-accepted';dataLayer.push({'event':eventName});}}",
            onInit: "window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('consent','default',{'ad_storage':'denied','analytics_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','wait_for_update':500});gtag('set','ads_data_redaction',true);"
          },
          {
            name: 'Session cookies',
            purposes: ['functional'],
            required: true,
            onAccept: "window.cookieMenager.set('cookieAccepted', true, {expires: 30 * 24 * 60 * 60 * 1000})"
          },
          {
            name: 'Facebook login',
            purposes: ['functional'],
            default: true,
            onAccept: "window.cookieMenager.set('facebook-login', true, {expires: 30 * 24 * 60 * 60 * 1000})",
            onDecline: "window.cookieMenager.set('facebook-login', false, {expires: 30 * 24 * 60 * 60 * 1000})"
          },
          {
            name: 'Google login',
            purposes: ['functional'],
            default: true,
            onAccept: "window.cookieMenager.set('google-login', true, {expires: 30 * 24 * 60 * 60 * 1000})",
            onDecline: "window.cookieMenager.set('google-login', false, {expires: 30 * 24 * 60 * 60 * 1000})"
          },
          {
            name: 'Google analytics',
            cookies: [/^_ga(_.*)?/],
            purposes: ['analytics'],
            onAccept: "window.cookieMenager.set('google-analytics', true, {expires: 30 * 24 * 60 * 60 * 1000})",
            onDecline: "window.cookieMenager.set('google-analytics', false, {expires: 30 * 24 * 60 * 60 * 1000})"
          }
        ]
      });
    }
  };

  const getCookie = (name: string) => {
    if (typeof document !== 'undefined') {
      const cookies = document.cookie.split('; ');
      for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
          return decodeURIComponent(value);
        }
      }
    }
    return null;
  };

  const setCookie = (name: string, value: string, attributes?: CookieAttributes) => {
    if (typeof document !== 'undefined') {
      let cookieString = encodeURIComponent(name) + '=' + encodeURIComponent(value);
      if (attributes) {
        for (const [key, val] of Object.entries(attributes)) {
          cookieString += `; ${key}=${val}`;
        }
      }
      document.cookie = cookieString;
    }
  };

  React.useEffect(() => {
    setupKlaro();
  }, []);

  return (
    <div>
      <h1>Cookie Information</h1>
      <p>We use cookies to ensure you get the best experience on our website.</p>
    </div>
  );
};

export default CookieInformation;