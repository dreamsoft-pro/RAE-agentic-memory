/**
 * Service: sitemap
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Translate } from 'react-translate-component'; // Assuming you have a library for translations

interface SiteMapProps {
  sites: any[];
  currentLang: { code: string };
  site: {
    groups: any[];
    types: any[];
    langs: { [key: string]: { url: string; name: string } };
  };
}

const SiteMap: React.FC<SiteMapProps> = ({ sites, currentLang, site }) => {
  return (
    <div className="container" id="content-sitemap">
      <div className="row">
        <h1 className="page-header"><Translate content="site_map" /></h1>
        <div className="col-md-12">
          {site.groups && (
            <ul>
              {site.groups.map((group, index) => (
                <li key={index}>
                  <a href="#" ui-sref="group({categoryurl: site.langs[currentLang.code].url, groupurl: group.slugs[currentLang.code]})" title={group.names[currentLang.code]}>
                    {group.names[currentLang.code]}
                  </a>
                  {group.types && (
                    <ul>
                      {group.types.map((type, idx) => (
                        <li key={idx}>
                          <a href="#" ui-sref="calculate({categoryurl: site.langs[currentLang.code].url, groupurl: type.group.slugs[currentLang.code], typeurl: type.slugs[currentLang.code]})" title={type.names[currentLang.code]}>
                            {type.names[currentLang.code]}
                          </a>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              ))}
            </ul>
          )}
          {site.types && (
            <ul>
              {site.types.map((type, index) => (
                <li key={index}>
                  <a href="#" ui-sref="calculate({categoryurl: site.langs[currentLang.code].url, groupurl: type.group.slugs[currentLang.code], typeurl: type.slugs[currentLang.code]})" title={type.names[currentLang.code]}>
                    {type.names[currentLang.code]}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default SiteMap;