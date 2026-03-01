/**
 * Service: SelectProjectCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getOneForView, getProjectsForTypes } from './services/PsTypeService';
import { Notification } from './Notification';
import { PhotoFolderService } from './services/PhotoFolderService';

const SelectProjectCtrl: React.FC = () => {
    const { typeurl, groupurl } = useParams<{ typeurl: string; groupurl: string }>();
    const [type, setType] = useState({});
    const [mainThemes, setMainThemes] = useState([]);

    useEffect(() => {
        init();
    }, []);

    async function init() {
        try {
            const dataType = await getOneForView(groupUrl, typeUrl);
            setType(dataType);

            const formats = [];
            const data = await PhotoFolderService.getProjectsForTypes(formats);
            setMainThemes(data);
        } catch (error) {
            Notification.error("Error fetching data");
        }
    }

    return (
        <div>
            {/* Render your UI here */}
        </div>
    );
};

export default SelectProjectCtrl;
