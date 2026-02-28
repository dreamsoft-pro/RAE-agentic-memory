/**
 * Service: ngGallery
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import styles from './ngGallery.module.css';

const NgGallery = ({ images, thumbsNum, hideOverflow }) => {
    const [index, setIndex] = useState(0);
    const [opened, setOpened] = useState(false);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    const openGallery = (i) => {
        if (typeof i !== 'undefined') {
            setIndex(i);
        }
        setOpened(true);
        if (hideOverflow) {
            document.body.style.overflow = 'hidden';
        }
    };

    const closeGallery = () => {
        setOpened(false);
        if (hideOverflow) {
            document.body.style.overflow = '';
        }
    };

    const loadImage = async (i) => {
        return new Promise((resolve, reject) => {
            const image = new Image();
            image.onload = () => {
                setLoading(false);
                if (image.naturalWidth === 0 || image.complete === false) {
                    reject();
                } else {
                    resolve(image);
                }
            };
            image.onerror = () => reject();
            image.src = images[i].img;
        });
    };

    const showImage = async (i) => {
        try {
            const img = await loadImage(i);
            setImg(img.src);
            smartScroll(i);
        } catch (error) {
            console.error('Error loading image:', error);
        }
    };

    useEffect(() => {
        if (opened) {
            document.addEventListener('keydown', handleKeyDown);
        } else {
            document.removeEventListener('keydown', handleKeyDown);
        }
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [opened]);

    const handleKeyDown = (event) => {
        if (event.keyCode === 27) { // ESC key
            closeGallery();
        } else if (event.keyCode === 39 || event.keyCode === 13) { // right or enter key
            nextImage();
        } else if (event.keyCode === 37) { // left key
            prevImage();
        }
    };

    const calculateThumbsWidth = () => {
        let width = 0, visible_width = 0;
        images.forEach((img) => {
            width += img.thumb.clientWidth;
            width += 10; // margin-right
            visible_width = img.thumb.clientWidth + 10;
        });
        return { width: width, visible_width: visible_width * (thumbsNum || 3) };
    };

    const smartScroll = (index) => {
        setTimeout(() => {
            const len = images.length;
            const item_scroll = Math.ceil(calculateThumbsWidth().visible_width / len);
            const s = Math.ceil(len / item_scroll);
            document.querySelector('.ng-thumbnails-wrapper').scrollLeft = 0;
            document.querySelector('.ng-thumbnails-wrapper').scrollLeft = index * item_scroll - (s * item_scroll);
        }, 100);
    };

    const nextImage = () => {
        setIndex((prevIndex) => (prevIndex + 1) % images.length);
        showImage(index);
    };

    const prevImage = () => {
        setIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
        showImage(index);
    };

    return (
        <div className={styles.baseClass}>
            <div>
                {images.map((img, i) => (
                    <img key={i} src={img.thumb} alt={`Image ${i + 1}`} onClick={() => openGallery(i)} />
                ))}
            </div>
            {opened && (
                <div className={styles.ngOverlay}>
                    <div className={loading ? styles.uilRingCss : ''}>
                        {!loading && (
                            <>
                                <a href={images[index].downloadSrc} target="_blank" className={styles.downloadImage}>
                                    <i className="fa fa-download"></i>
                                </a>
                                <a onClick={closeGallery} className={styles.closePopup}>
                                    <i className="fa fa-close"></i>
                                </a>
                                <a onClick={prevImage} className={styles.navLeft}>
                                    <i className="fa fa-angle-left"></i>
                                </a>
                                <img src={img} onDragStart={(e) => e.preventDefault()} draggable={false} onClick={nextImage} className={styles.effect} />
                                <a onClick={nextImage} className={styles.navRight}>
                                    <i className="fa fa-angle-right"></i>
                                </a>
                                <span className={styles.infoText}>{index + 1}/{images.length} - {images[index].description}</span>
                                <div className={styles.ngThumbnailsWrapper}>
                                    <div className={styles.ngThumbnailsSlideLeft}>
                                        {images.map((img, i) => (
                                            <img key={i} src={img.thumb} alt={`Image ${i + 1}`} className={index === i ? styles.active : ''} onClick={() => changeImage(i)} />
                                        ))}
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NgGallery;
