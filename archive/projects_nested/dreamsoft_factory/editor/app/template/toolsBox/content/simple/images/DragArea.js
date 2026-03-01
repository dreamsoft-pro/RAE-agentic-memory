import React from 'react';

const DragArea = ({loadFiles, setIsDraggingFile}) => {
    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        loadFiles(e.dataTransfer.files);
        handleDragLeave(e);
    };

    const handleDragLeave = (e) => {
        e.stopPropagation();
        setIsDraggingFile(false);
    };

    return (
        <div
            id="imageDrop"
            data-type="image"
            onDrop={(e) => handleDrop(e)}
            onDragLeave={(e) => handleDragLeave(e)}
        >
            <div className={'image-drop-inner'}>
                <div className={'image-drop-icon'}></div>
                <div>Upuść zdjęcia tutaj!</div>
            </div>
        </div>
    );
};

export default DragArea;
