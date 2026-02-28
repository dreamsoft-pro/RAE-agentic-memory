import React, {useEffect, useState} from 'react';
import ButtonsContainer from "./ButtonsContainer";
import ImagesScrollContainer from "./ImagesScrollContainer";
import MiniatureAndUploadInfo from "./MiniatureAndUploadInfo";
import DragArea from "./DragArea";
import useUploadUserImages from "../../../../../hooks/UploadUserImages";
import {useSelector} from "react-redux";
import EffectsToolContent from "../../../../canvasToolsBox/images/effects/EffectsToolContent";
import PositionsToolContent from "../../../../canvasToolsBox/images/positions/PositionsToolContent";
import image from "./Image";

const ImagesToolContent = ({editor, className}) => {
    const {data, loadFiles} = useUploadUserImages(editor);
    const [isDraggingFile, setIsDraggingFile] = useState(false);
    const {editorType} = useSelector(state => state.projectReducer)
    const {selectedImage} = useSelector(state => state.selectedImageReducer)

    const handleDragOver = (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';

        setIsDraggingFile(true);
    }

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDraggingFile(false);
    }

    return (
        <div
            id={"imagesContent"}
            className={`inner-container ${className}`}
            onDragOver={(e) => handleDragOver(e)}
            onDragLeave={(e) => handleDragLeave(e)}
        >
            {!selectedImage.effects && !selectedImage.position && (
                <>
                    {isDraggingFile && <DragArea editor={editor} loadFiles={loadFiles} setIsDraggingFile={setIsDraggingFile}/>}
                    <ButtonsContainer editor={editor} loadFiles={loadFiles} data={data}/>
                    <ImagesScrollContainer editor={editor}/>
                </>
            )}
            {(selectedImage.effects || selectedImage.position) && (selectedImage.effects ?
                <EffectsToolContent editor={editor}/>
                :
                <PositionsToolContent/>
            )}

            <MiniatureAndUploadInfo data={data}/>
        </div>
    )
}

export default ImagesToolContent
