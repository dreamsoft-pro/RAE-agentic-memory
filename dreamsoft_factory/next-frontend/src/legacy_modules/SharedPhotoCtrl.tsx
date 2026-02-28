/**
 * Service: SharedPhotoCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PhotoFolderService } from './services/PhotoFolderService';
import Notification from './Notification';

const SharedPhotoCtrl: React.FC = () => {
    const { photoid, source } = useParams();
    const [photo, setPhoto] = useState<any>({});
    const navigate = useNavigate();

    const init = async () => {
        console.log(photoid);
        console.log(source);

        if (source === 'mail') {
            // Handle mail source logic here
        } else if (source === 'facebook') {
            try {
                const data = await PhotoFolderService.getPhotoSharedByFacebook(photoid);
                setPhoto(data);
            } catch (error) {
                console.error('Error fetching photo from Facebook:', error);
            }
        }
    };

    React.useEffect(() => {
        init();
    }, []);

    const handleSend = async () => {
        const password = form.password;
        try {
            const data = await PhotoFolderService.getPhotoSharedByEmail(photoid, password);
            setPhoto(data);
        } catch (error) {
            console.error('Error sending photo by email:', error);
        }
    };

    const handleSelectPhoto = (photo: any) => {
        setActualPhoto(photo);
    };

    return (
        <div>
            {/* Render your UI components here */}
        </div>
    );
};

export default SharedPhotoCtrl;
