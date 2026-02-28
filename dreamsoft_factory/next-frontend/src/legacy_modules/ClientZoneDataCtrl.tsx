/**
 * Service: ClientZoneDataCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import _ from 'lodash';
import { Notification } from '@mui/material'; // Assuming you are using Material-UI for notifications
import { DpAddressService, CountriesService, PhotoFolderService, UserService } from '../services'; // Adjust the import paths as necessary

const ClientZoneDataCtrl: React.FC = () => {
    const [form, setForm] = useState({});
    const [actualUser, setActualUser] = useState({ login: '' });
    const [countries, setCountries] = useState([]);
    const [photoForm, setPhotoForm] = useState({});
    const router = useRouter();

    useEffect(() => {
        init();
    }, []);

    const init = () => {
        getImportantData();
    };

    const getImportantData = async () => {
        try {
            const data = await UserService.getImportantData();
            setForm(data);
            setActualUser({ login: data.login });
            setForm((prev) => ({ ...prev, smsAgree: !!data.sms, advAgree: !!data.advertising }));
            showCountries(data.countryCode);
        } catch (error) {
            console.error("Error fetching important data:", error);
        }
    };

    const showCountries = async (countryCode: string) => {
        try {
            const dataCountries = await CountriesService.getAll();
            setCountries(dataCountries);
        } catch (error) {
            console.error("Error fetching countries:", error);
        }
    };

    const edit = async () => {
        const data = _.cloneDeep(form);
        data.sms = data.smsAgree ? 1 : 0;
        delete data.smsAgree;
        data.advertising = data.advAgree ? 1 : 0;
        delete data.advAgree;

        try {
            const response = await UserService.editImportantData(data);
            if (response.response === true) {
                console.log('Successfully edited'); // Assuming you have a way to display notifications
            } else {
                console.error('Error editing data'); // Assuming you have a way to display notifications
            }
        } catch (error) {
            console.error('Error:', error); // Assuming you have a way to display notifications
        }
    };

    const addPhotoFolder = () => {
        console.log(photoForm);
        PhotoFolderService.add(photoForm.name).then((data) => {
            console.log(data);
        });
    };

    const getFolders = async () => {
        try {
            const data = await PhotoFolderService.get();
            setFolders(data);
        } catch (error) {
            console.error("Error fetching photo folders:", error);
        }
    };

    const isCountryCode = () => {
        const country = _.find(countries, { code: form.countryCode });
        return country && String(country.areaCode).length > 0;
    };

    const updateAreaCode = () => {
        const country = _.find(countries, { code: form.countryCode });
        setForm((prev) => ({ ...prev, areaCode: country.areaCode }));
    };

    return (
        <div>
            {/* Your component JSX here */}
        </div>
    );
};

export default ClientZoneDataCtrl;