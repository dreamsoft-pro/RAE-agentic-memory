import React, {useState, useEffect} from 'react';

// Components providing sortable list of uploaded images
const ReorderImagesButton = ({editor, usedInModal = false, ...props}) => {
    const [showPopup, setShowPopup] = useState(false);

    const handleButtonClick = (e) => {
        e.stopPropagation();
        setShowPopup(true);
    };

    const handleClosePopup = (e) => {
        if (
            !$(e.target).hasClass('projectImage') &&
            !$(e.target).hasClass('projectImageContainer') &&
            !$(e.target).hasClass('imageMover') &&
            !$(e.target).hasClass('imageOrder')
        ) {
            setShowPopup(false);
        }
    };

    useEffect(() => {
        if (showPopup) {
            const imagesContainer = $('.projectImagesContainer');
            imagesContainer.sortable({
                stop: function () {
                    const elemArray = imagesContainer.sortable("toArray", {attribute: 'uid'});
                    editor.webSocketControllers.userProject.sortProjectImages(
                        elemArray,
                        editor.userProject.getID()
                    );
                }
            });
            imagesContainer.disableSelection();
        }
    }, [showPopup, editor]);

    const getSortedImages = () => {
        const images = editor.userProject.getProjectImages();
        return Object.values(images).sort((a, b) => a.imageOrder - b.imageOrder);
    };

    return (
        <>
            <button
                {...props}
                className={`reorderImagesButton default-button ${usedInModal ? 'disable-actions' : ''}`}
                onClick={(e) => !usedInModal ? handleButtonClick(e) : {}}
            />

            {!usedInModal && showPopup && (
                <div className="totalWhitePopUp" onClick={(e) => handleClosePopup(e)}>
                    <h4>Ustaw zdjęcia w kolejności, potem użyj autouzupełniania</h4>
                    <div className="projectImagesContainer">
                        {getSortedImages().map((image, index) => (
                                <SortableImage
                                    key={index}
                                    image={image}
                                />
                            )
                        )}
                    </div>
                </div>
            )}
        </>
    );
};


// Single sortable image component
const SortableImage = ({image}) => {
    const {uid, thumbnail, imageOrder} = image

    const backgroundImageUrl = thumbnail.startsWith('http') ? thumbnail : `${EDITOR_ENV.staticUrl}${thumbnail}`;

    return (
        <div className="projectImageContainer" uid={uid}>
            <div
                className="projectImage"
                style={{backgroundImage: `url(${backgroundImageUrl})`}}
            ></div>
            <div className={'projectImageInnerContainer'}>
                <div className="imageViewer"></div>
                <div className="imageOrder">{imageOrder || '.'}</div>
                <div className="imageMover"></div>
            </div>
        </div>
    );
}

export default ReorderImagesButton;
