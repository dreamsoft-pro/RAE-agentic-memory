/**
 * Service: ReclamationsCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useHistory } from 'react-router-dom';
import { getReclamations, countReclamations } from './reclamationActions';
import { formatSizeUnits } from './formatUtils';
import { getMessages } from './messageService';
import { uploadFile } from './fileUploader';
import { ReclamationService } from './services/ReclamationService';
import { MainWidgetService } from './services/MainWidgetService';
import { TemplateRootService } from './services/TemplateRootService';
import { Notification } from 'react-notification';
import socketClient from 'socket.io-client';
import AuthDataService from './services/AuthDataService';
import config from './config';

const ReclamationsCtrl: React.FC = () => {
    const [reclamations, setReclamations] = useState([]);
    const [pagingSettings, setPagingSettings] = useState({ total: 0 });
    const [currentPage, setCurrentPage] = useState(1);
    const [params, setParams] = useState({});
    const dispatch = useDispatch();
    const history = useHistory();
    const { page } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            await getReclamations(dispatch, currentPage, params);
        };
        fetchData();
    }, [currentPage, params, dispatch]);

    useEffect(() => {
        if (reclamations.length > 0) {
            setPagingSettings({ total: count });
        }
    }, [reclamations]);

    const handleNextPage = () => {
        setCurrentPage(prevPage => prevPage + 1);
    };

    const handlePreviousPage = () => {
        setCurrentPage(prevPage => prevPage - 1);
    };

    const formatSizeUnits = (file: any) => MainWidgetService.formatSizeUnits(file.size);

    const getMessagesFromServer = (reclamationID: string) => {
        ReclamationService.getMessages(reclamationID).then((data: any) => {
            setMessages(data);
        });
    };

    const handleReclamationSelection = (reclamation: any) => {
        TemplateRootService.getTemplateUrl(101).then((response: any) => {
            openModal({
                templateUrl: response.url,
                scope: this,
                size: 'lg',
                controller: (ctx: any) => {
                    ctx.reclamation = reclamation;
                    ctx.messages = [];
                    socket.emit('onReclamation', { reclamationID: reclamation.ID });
                }
            });
        });
    };

    const handleSendMessage = (reclamation: any) => {
        socket.emit('addMessage', {
            reclamationID: reclamation.ID,
            message: this.form.message,
            accessToken: AuthDataService.getAccessToken(),
            companyID: $rootScope.companyID
        });
    };

    const handleUpload = () => {
        changeUrl(selectedReclamation.ID).then(() => {
            uploadFile();
            ReclamationService.getFiles(selectedReclamation.ID).then((filesData: any) => {
                const idx = reclamations.findIndex(({ ID }: any) => ID === selectedReclamation.ID);
                if (idx > -1) {
                    reclamations[idx].files = filesData;
                }
                setSelectedReclamation(null);
                clearQueue();
                setUploadProgress(0);
                Notification.success('File uploaded successfully');
            });
        });
    };

    const handleCancelUpload = () => {
        clearQueue();
        setSelectedReclamation(null);
    };

    return (
        <div>
            {/* Render your UI components here */}
        </div>
    );
};

export default ReclamationsCtrl;