import React from 'react'
import {setCurrentSelectedImageToolIndex} from "../../../../redux/reducers/images/selectedImage";
import {useSelector} from "react-redux";
import {store} from "../../../../ReactSetup";
import ToolButton from './ToolButton';
import MasksContent from './MasksContent';
import FrameContent from './FrameContent';
import ImageEffects from "./ImageEffects";
import ShadowContent from './ShadowContent';
import FrameUnderPhotoContent from "./FrameUnderPhotoContent";


const EffectsToolContent = ({editor}) => {
    const { currentToolIndex } = useSelector(state => state.selectedImageReducer)

    const selectedImageToolsButtons = [
        'image-frame',
        'under-image-frame',
        'image-shadow',
        'image-masks',
        'image-effects'
    ]

    const renderTool = (currentToolIndex) => {
        switch(currentToolIndex) {
            case 0: return <FrameContent editor={editor}/>;
            case 1: return <FrameUnderPhotoContent />;
            case 2: return <ShadowContent />;
            case 3: return <MasksContent />;
            case 4: return <ImageEffects />;
            
            default: return <h1>No tool match</h1>
        }
    }

    return (
        <div className={'selected-item-tools-container'}>
            <div className={'tools-buttons-container'}>
                {selectedImageToolsButtons.map((tool, index) => (
                    <ToolButton
                        key={index}
                        className={`selected-item-tool-button ${tool}`}
                        onClick={() => store.dispatch(setCurrentSelectedImageToolIndex(index))}
                        isActive={currentToolIndex === index}
                    />
                ))}
            </div>
            <div className={'selected-item-tool-content-container'}>
                { renderTool(currentToolIndex) }
            </div>
        </div>
    )
}

export default EffectsToolContent