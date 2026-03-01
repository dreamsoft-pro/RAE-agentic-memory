import { useEffect, useState} from 'react'
import {ProjectImage} from "../class/ProjectImage";
import {addProjectImage} from "../redux/reducers/images/images";
import {store} from "../ReactSetup";

const useUploadUserImages = (editor) => {
    const [isUploading, setIsUploading] = useState(false);
    const [isUploadingFinished, setIsUploadingFinished] = useState(false);
    const [files, setFiles] = useState([])

    const loadFiles = (files) => {
        setFiles(Array.from(files))
    }

    useEffect(() => {
        if (files.length) {
            setIsUploading(true);

            const imagesCount = files.length;

            let totalSizeToUpload = calculateTotalUploadSize(files);
            let currentFileIndex = 0;
            let uploadedImagesCount = 0;

            updatePhotosCounter(imagesCount);
            updateUploadInfo(totalSizeToUpload, imagesCount);

            function calculateTotalUploadSize(files) {
                return Array.from(files).reduce((total, file) => total + file.size, 0);
            }

            function updatePhotosCounter(imagesCount) {
                const counterElement = $('.projectPhotosCounter');
                const currentCount = editor.userProject.getImageCounter();
                const newCount = currentCount + imagesCount;
                counterElement.attr('count', newCount).html(`Zdjęć: ${newCount}`);
            }

            function updateUploadInfo(toUpload, imagesCount) {
                const uploadInfoText = $('.miniaturesInfo .uploadInfoLoaderText');
                if (uploadInfoText.html() === "") {
                    uploadInfoText.html(`0/${imagesCount}`).attr('allImages', imagesCount);
                    $('.uploadingInfo .uploadInfoLoaderText').attr('to-upload', toUpload);
                } else {
                    const [uploaded, total] = uploadInfoText.html().split('/').map(Number);
                    uploadInfoText.html(`${uploaded}/${total + imagesCount}`);
                    const previousToUpload = parseInt($('.uploadingInfo .uploadInfoLoaderText').attr('to-upload'));
                    $('.uploadingInfo .uploadInfoLoaderText').attr('to-upload', previousToUpload + toUpload);
                }
            }

            function uploadImage() {
                const file = files[currentFileIndex];
                const url = URL.createObjectURL(file);
                const imageElement = new Image();
                imageElement.src = url;

                imageElement.onload = function () {
                    URL.revokeObjectURL(url);
                    handleImageUpload(file, imageElement);
                    incrementImageUploadProgress();
                };
            }

            function handleImageUpload(file, imageElement) {
                const isSVG = file.name.endsWith('.svg');
                const bitmap = new createjs.Bitmap(imageElement);

                if (isSVG) {
                    processSvgImage(bitmap, file);
                } else {
                    processBitmapImage(bitmap, file);
                }

                if (currentFileIndex < imagesCount - 1) {
                    currentFileIndex++;
                    uploadImage();
                }
            }

            function processSvgImage(bitmap, file) {
                bitmap.origin = bitmap.getBounds();
                const aspectRatio = bitmap.origin.width / bitmap.origin.height;

                // Set up bitmap properties for display
                bitmap.x = 900 / 2;
                bitmap.y = 400 / 2;
                bitmap.scaleX = Editor.settings.thumbSize * aspectRatio / bitmap.origin.width;
                bitmap.scaleY = Editor.settings.thumbSize / bitmap.origin.height;
                bitmap.regX = bitmap.trueWidth = bitmap.origin.width / 2;
                bitmap.regY = bitmap.trueHeight = bitmap.origin.height / 2;
                bitmap.name = file.name;

                // Create a simple image instance
                const projectImage = new ProjectImage();
                projectImage.editor = Editor;
                projectImage.thumbnail = bitmap;
                projectImage.minUrl = bitmap;
                projectImage.waitingForUpload = true;
                Editor.userProject.increaseImageCounter();

                // Initialize simple image and add to user simple
                projectImage.initForUser(
                    file, bitmap, bitmap,
                    bitmap.origin.width, bitmap.origin.height,
                    bitmap.origin.width, bitmap.origin.height,
                    Editor.userProject.getImageCounter()
                );
                projectImage.minSize = {width: bitmap.origin.width, height: bitmap.origin.height};
                projectImage.thumbSize = {width: bitmap.origin.width, height: bitmap.origin.height};

                Editor.userProject.addProjectImage(projectImage);
                store.dispatch(addProjectImage(projectImage))

                // Handle uploading via WebSocket
                Editor.webSocketControllers.userProject.addPhoto(
                    projectImage.uid, Editor.userProject.getID(), file.name,
                    'Bitmap', null, null, null,
                    projectImage.width, projectImage.height,
                    projectImage.trueWidth, projectImage.trueHeight
                );

                Editor.uploader.addItemToUpload(projectImage);
                Editor.uploader.upload();

                // Set up event listeners for further image processing after upload
                projectImage.addEventListener('uploaded', function (data) {
                    const projectImageData = data.target;
                    const dataToUpload = {
                        projectImageUID: projectImageData.uid,
                        minUrl: projectImageData.miniatureUrl,
                        thumbnail: projectImageData.thumbnail,
                        imageUrl: projectImageData.imageUrl,
                        uploadID: projectImageData.uploadID
                    };
                    Editor.webSocketControllers.projectImage.update(dataToUpload);
                });
            }

            function processBitmapImage(bitmap, file) {
                bitmap.origin = bitmap.getBounds();
                bitmap.scale = {x: bitmap.origin.width, y: bitmap.origin.height};

                // Generate thumbnail using ThumbsMaker
                const thumbData = Editor.ThumbsMaker.generateThumb(bitmap);
                const thumbBitmap = new createjs.Bitmap(thumbData.min);

                thumbBitmap.image.onload = function () {
                    const origin = thumbBitmap.getBounds();
                    const aspectRatio = origin.width / origin.height;

                    thumbBitmap.x = 900 / 2;
                    thumbBitmap.y = 400 / 2;
                    thumbBitmap.scaleX = Editor.settings.thumbSize * aspectRatio / origin.width;
                    thumbBitmap.scaleY = Editor.settings.thumbSize / origin.height;
                    thumbBitmap.regX = thumbBitmap.trueWidth = thumbData.width / 2;
                    thumbBitmap.regY = thumbBitmap.trueHeight = thumbData.height / 2;
                    thumbBitmap.name = file.name;

                    // Create and initialize the simple image
                    const projectImage = new ProjectImage();
                    projectImage.editor = Editor;
                    projectImage.thumbnail = thumbData.thumb;
                    projectImage.minUrl = thumbData.min;
                    projectImage.waitingForUpload = true;
                    Editor.userProject.increaseImageCounter();

                    projectImage.initForUser(
                        file, thumbData.min, thumbData.thumb,
                        bitmap.origin.width, bitmap.origin.height,
                        origin.width, origin.height,
                        Editor.userProject.getImageCounter()
                    );

                    projectImage.minSize = thumbData.minSize;
                    projectImage.thumbSize = thumbData.thumbSize;

                    Editor.userProject.addProjectImage(projectImage);
                    store.dispatch(addProjectImage(projectImage))

                    // Handle uploading via WebSocket
                    Editor.webSocketControllers.userProject.addPhoto(
                        projectImage.uid, Editor.userProject.getID(), file.name,
                        'Bitmap', null, null, null,
                        projectImage.width, projectImage.height,
                        projectImage.trueWidth, projectImage.trueHeight
                    );

                    Editor.uploader.addItemToUpload(projectImage);
                    Editor.uploader.upload();

                    // Set up event listeners for further image processing after upload
                    projectImage.addEventListener('uploaded', function (data) {
                        const projectImageData = data.target;
                        const dataToUpload = {
                            projectImageUID: projectImageData.uid,
                            minUrl: projectImageData.miniatureUrl,
                            thumbnail: projectImageData.thumbnail,
                            imageUrl: projectImageData.imageUrl,
                            uploadID: projectImageData.uploadID
                        };
                        Editor.webSocketControllers.projectImage.update(dataToUpload);
                    });
                };
            }

            function incrementImageUploadProgress() {
                uploadedImagesCount++;
                $('.miniaturesInfo .uploadInfoLoaderText').html(`${uploadedImagesCount}/${imagesCount}`);
                $('.miniaturesInfo .uploadInfoLoaderProgress').width((uploadedImagesCount / imagesCount) * 100 + "%");

                if (uploadedImagesCount === imagesCount) {
                    // show user that he can already start designing his simple
                    const timeout = 3000;
                    setIsUploading(false);
                    setIsUploadingFinished(true);

                    $('.miniaturesInfo').addClass('hidden');
                    $('.miniaturesSuccessInfo').removeClass('hidden');

                    setTimeout(() => {
                        $('.miniaturesSuccessInfo').addClass('hidden');
                        setIsUploadingFinished(false);
                    }, timeout);

                } else {
                    $('.miniaturesInfo').removeClass('hidden');
                }
            }

            uploadImage();
        }
    }, [files]);


    return {
        loadFiles,
        data: {
            isUploadingFinished,
            isUploading
        },
    };
}

export default useUploadUserImages