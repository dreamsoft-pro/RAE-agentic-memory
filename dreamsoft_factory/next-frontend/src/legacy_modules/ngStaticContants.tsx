/**
 * Service: ngStaticContants
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import _ from 'lodash';
import { StaticContentService, $rootScope } from '@services'; // Assuming these are your services and root scope

const NgStaticContents: React.FC<{ content: string }> = ({ content }) => {
    const [contentObject, setContentObject] = React.useState({ contents: {} });

    React.useEffect(() => {
        const fetchContent = async () => {
            const data = await StaticContentService.getContent(content);
            const contents = {};

            if ($rootScope.currentLang) {
                contents[$rootScope.currentLang.code] = '';
            }

            _.each(data.contents, (content, lang) => {
                contents[lang] = content;
            });

            setContentObject({ contents });
        };

        fetchContent();
    }, [content]);

    return <div data-ta-bind={`ng-model="contentObject.contents[$root.currentLang.code]"`} />;
};

export default NgStaticContents;