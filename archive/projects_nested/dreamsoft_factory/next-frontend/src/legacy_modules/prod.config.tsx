/**
 * Service: prod.config
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

type ConfigOptions = {
  apiUrl: string;
  authUrl: string;
  staticUrl: string;
  socketUrl: string;
  editorUrl: string;
  id: string;
  domainID: string;
  gaCodes: { [key: string]: string };
  mainFolders: { [key: string]: string };
  seo: { [key: string]: { title: string; description: string; keywords: string } };
  googleWebTools: { [key: string]: string };
};

const createConfig = (appOptions: Partial<ConfigOptions>): ConfigOptions => ({
  apiUrl: appOptions.apiUrl || 'http://localtest.me/api/',
  authUrl: appOptions.authUrl || 'http://authapp.localtest.me/',
  staticUrl: appOptions.staticUrl || 'http://localtest.me/static/',
  socketUrl: appOptions.socketUrl || 'http://authapp.localtest.me',
  editorUrl: appOptions.editorUrl || 'http://editor.localtest.me/',
  id: appOptions.id || '25',
  domainID: appOptions.domainID || '2',
  gaCodes: { ...(appOptions.gaCodes || { default: '$INDEX_GA_CODE' }) },
  mainFolders: { ...(appOptions.mainFolders || { default: 'dist' }) },
  seo: { ...(appOptions.seo || { default: { title: '$INDEX_SEO_TITLE', description: '$INDEX_SEO_DESCRIPTION', keywords: '$INDEX_SEO_KEYWORDS' } }) },
  googleWebTools: { ...(appOptions.googleWebTools || { default: '$INDEX_SEARCH_CONSOLE_CODE' }) },
});

const getConfig = (appOptions?: Partial<ConfigOptions>): ConfigOptions => {
  return createConfig(appOptions || {});
};

export default getConfig;