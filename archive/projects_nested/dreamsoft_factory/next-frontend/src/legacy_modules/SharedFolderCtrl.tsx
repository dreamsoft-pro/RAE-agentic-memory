/**
 * Service: SharedFolderCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { PhotoFolderService } from './services/PhotoFolderService';
import Notification from './Notification';

const SharedFolderCtrl: React.FC = () => {
    const [folderId] = useState<string | undefined>(useParams().folderid);
    const [source] = useState<string | undefined>(useParams().source);
    const [folder, setFolder] = useState({});
    const [photos, setPhotos] = useState<any[]>([]);
    const history = useHistory();

    const [rating, setRating] = useState({ current: 0, max: 5 });
    const [actualPhoto, setActualPhoto] = useState({});

    const getSelectedRating = (rating: number) => {
        console.log(rating);
    };

    useEffect(() => {
        if (source === 'mail') {
            PhotoFolderService.getSharedByEmail(folderId).then((data) => {
                console.log(data);
            });
        } else if (source === 'facebook') {
            PhotoFolderService.getSharedByFacebook(folderId).then((data) => {
                setFolder(data);
                setPhotos(data.imageFiles);
            });
        }
    }, [source, folderId]);

    const send = () => {
        const password = (document.querySelector('#password') as HTMLInputElement)?.value;
        PhotoFolderService.getSharedByEmail(folderId, password).then((data) => {
            setFolder(data);
            setPhotos(data.imageFiles);
        });
    };

    const selectPhoto = (photo: any) => {
        setActualPhoto(photo);
    };

    const nextPhoto = (photo: any) => {
        const idx = photos.findIndex((p) => p._id === photo._id);
        if (idx > -1 && photos[idx + 1]) {
            setActualPhoto(photos[idx + 1]);
        }
    };

    const previousPhoto = (photo: any) => {
        const idx = photos.findIndex((p) => p._id === photo._id);
        if (idx > -1 && photos[idx - 1]) {
            setActualPhoto(photos[idx - 1]);
        }
    };

    const nextExist = (photo: any) => {
        const idx = photos.findIndex((p) => p._id === photo._id);
        if (idx > -1 && photos[idx + 1]) {
            return true;
        }
        return false;
    };

    const previousExist = (photo: any) => {
        const idx = photos.findIndex((p) => p._id === photo._id);
        if (idx > -1 && photos[idx - 1]) {
            return true;
        }
        return false;
    };

    return (
        <div>
            <div>{JSON.stringify(folder)}</div>
            <div>{photos.map((photo) => (
                <div key={photo._id} onClick={() => selectPhoto(photo)}>
                    {photo.name}
                </div>
            ))}</div>
            <button onClick={nextPhoto}>Next Photo</button>
            <button onClick={previousPhoto}>Previous Photo</button>
        </div>
    );
};

export default SharedFolderCtrl;