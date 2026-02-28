/**
 * Service: SharedProjectCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { EditorProjectService, Notification, $filter } from './services'; // Adjust the import paths accordingly

const SharedProjectCtrl = () => {
    const { projectid: projectId } = useParams();
    const [source, setSource] = useState('');

    useEffect(() => {
        setSource(projectId);
    }, [projectId]);

    const send = async () => {
        try {
            const data = await EditorProjectService.shareMyProject(form.email, projectId);
            Notification.success($filter('translate')('success'));
        } catch (error) {
            Notification.error($filter('translate')('error'));
        }
    };

    const sendFb = async () => {
        try {
            const data = await EditorProjectService.shareMyProjectByFb(projectId);
            if (data.link) {
                Notification.success($filter('translate')('success'));
                window.location.href = `http://${data.link}`;
            } else {
                Notification.error($filter('translate')('error'));
            }
        } catch (error) {
            Notification.error($filter('translate')('error'));
        }
    };

    return (
        <div>
            {/* React components and JSX elements can be added here */}
        </div>
    );
};

export default SharedProjectCtrl;
