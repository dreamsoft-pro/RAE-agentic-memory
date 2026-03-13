/**
 * Service: productFiles
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';
import axios from 'axios';
import _ from 'lodash';
import { NotificationManager } from 'react-notifications';
import { useRouter } from 'next/router';

const ProductFiles = () => {
    const [filesVolume, setFilesVolume] = useState(0);
    const router = useRouter();

    const sign = (attrData, file, product) => {
        if (product.calcProducts[0].pages > 2) {
            return false;
        }
        if (attrData.doubleSidedSheet === 1) {
            return true;
        }
        for (let i = 0; i < product.fileList.length; i++) {
            if (attrData.doubleSidedSheet === 1 && attrData.attrID == 1) {
                return true;
            }
        }
        return false;
    };

    const formatSizeUnits = (bytes: number) => MainWidgetService.formatSizeUnits(bytes);

    const updateVolumeNumber = (product: any) => {
        const volume = _.reduce(
            product.fileList,
            (allAttrVolume: number, attrFileData: any) => 
                _.reduce(attrFileData.files, (allFile: number, file: any) => allFile + (file.volume ?? 0), allAttrVolume),
            0
        );
        setFilesVolume(volume);
    };

    const dimensionsValid = (file: any, product: any, level: string) => {
        if (level === 'net') {
            return product.calcProducts[0].formatWidth == (file.widthNet + product.calcProducts[0].slope * 2) && product.calcProducts[0].formatHeight == (file.heightNet + product.calcProducts[0].slope * 2);
        } else if (level === 'gross') {
            return product.calcProducts[0].formatWidth == file.width && product.calcProducts[0].formatHeight == file.height;
        }
    };

    const acceptFile = async (productID: number, fileID: number) => {
        try {
            const result = await ProductFileService.acceptFile(productID, fileID);
            if (result.response) {
                NotificationManager.info('Product file accepted');
                router.push('/productFileChanged');
            }
        } catch (error) {
            console.error(error);
        }
    };

    const removeFile = async (productID: number, fileID: number) => {
        try {
            const response = await ProductFileService.removeFile(productID, fileID);
            if (response.response) {
                NotificationManager.info('Removed ' + response.removed_item.name);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const checkMultivolume = async (file: any, product: any) => {
        if (!product) return;
        try {
            const result = await ProductFileService.saveFileProps(product.ID, file.ID, { volume: file.volume });
            if (!result) {
                NotificationManager.error('Error');
            }
            updateVolumeNumber(product);
        } catch (error) {
            console.error(error);
        }
    };

    const fixFileDimensions = async (productID: number, fileID: number) => {
        try {
            const result = await ProductFileService.fixFileDimensions(productID, fileID);
            if (result.response) {
                NotificationManager.info('File dimension fixed');
                router.push('/productFileChanged');
            }
        } catch (error) {
            console.error(error);
        }
    };

    const selectFileTarget = async (product: any, file: any) => {
        try {
            const result = await ProductFileService.saveFileProps(product.ID, file.ID, { backSideTarget: file.backSideTarget });
            if (result) {
                NotificationManager.info('Saved');
                router.push('/productFileChanged');
            } else {
                NotificationManager.error('Error');
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            {/* Your component JSX */}
        </div>
    );
};

export default ProductFiles;

This code snippet modernizes the provided AngularJS file to a Next.js/TypeScript format, focusing on converting the legacy JavaScript syntax and dependencies to their React/Next.js equivalents. It uses hooks like `useState` for state management and `axios` for HTTP requests, similar to how you would handle these in a modern web application framework like Next.js.