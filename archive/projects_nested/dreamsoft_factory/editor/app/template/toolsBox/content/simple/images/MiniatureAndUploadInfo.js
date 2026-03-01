import React from 'react';
import {useSelector} from "react-redux";

const MiniatureAndUploadInfo = ({data}) => {
    const { images } = useSelector(state => state.imagesReducer)

    return (
        <div id="imageLoaderInfo">
            {/* Miniatures Info Section */}
            <div className="miniaturesInfo hidden">
                <span className="title">Wczytuję miniatury</span>
                <div className="uploadInfoLoader">
                    <div className="uploadInfoLoaderProgress"></div>
                    <div className="uploadInfoLoaderText"></div>
                </div>
            </div>
            <div className={'miniaturesSuccessInfo hidden'}>
                <span>
                    Miniatury zostały załadowane pomyślnie
                </span>
                <span>
                    Możesz zacząć projektować!
                </span>
            </div>

            {/*Uploading Info Section */}
            <div className="uploadingInfo hidden">
                <span className="title">Zapisywanie zdjęć</span>
                <div className="uploadInfoLoader">
                    <div className="uploadInfoLoaderProgress"></div>
                    <div className="uploadInfoLoaderText"></div>
                </div>
                <div className="estimation"></div>
            </div>
            <div className={'uploadingSuccessInfo hidden'}>
                <span>
                    Zdjęcia zostały załadowane
                </span>
            </div>

            {images.length > 0 && (
                <section className={"projectPhotosWrapper"}>
                    <div className="projectPhotosInfos">
                        <div className="projectPhotosCounter">Zdjęć: {images.length}</div>
                        <div className="projectNotUsedPhotosCounter">Użytych: {images.filter(image => image.used).length}</div>
                    </div>
                    <button
                        data-bs-toggle={"modal"}
                        data-bs-target={"#removeAllImagesModal"}
                        disabled={data.isUploading}
                        className={"allImagesRemover"}
                    >
                    </button>
                </section>
            )}
        </div>
    );
}

export default MiniatureAndUploadInfo