import React from 'react';
import { LayerUpButton } from './buttons/LayerUpButton';
import { LayerDownButton } from './buttons/LayerDownButton';
import { VerticalReflectButton } from './buttons/VerticalReflectButton';
import { HorizontalReflectButton } from './buttons/HorizontalReflectButton';
import { CenterOnPageButton } from './buttons/CenterOnPageButton';
import { FullPageButton } from './buttons/FullPageButton';
import { useSelector } from 'react-redux';


const PositionsWrapper = () => {

    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);

    console.log("POZYCJA PROPONOWANA", proposedPositionInstance)

    const onLayerDownClick = (e) => {
        e.stopPropagation();
        const editingObject = proposedPositionInstance;

        const index = editingObject.parent.getChildIndex(editingObject);

        if (index > 0) {

            editingObject.parent.setChildIndex(editingObject, index - 1);
            proposedPositionInstance.editor.webSocketControllers.userPage.moveObjectDown(proposedPositionInstance.dbID, proposedPositionInstance.getFirstImportantParent().userPage._id);

        }
        else if (editingObject.parent.name === 'foregroundLayer') {

            const background = editingObject.parent.parent.backgroundLayer;
            editingObject.parent.removeChild(editingObject);

            if (background.children.length > 0)
                background.addChildAt(editingObject, background.children.length - 1);
            else
                background.addChildAt(editingObject, background.children.length);

        }

    }

    const onLayerUpClick = (e) => {
        e.stopPropagation();
        const editingObject = proposedPositionInstance;

        const index = editingObject.parent.getChildIndex(editingObject);

        if (index < (editingObject.parent.children.length - 1)) {

            editingObject.parent.setChildIndex(editingObject, index + 1);
            editingObject.order = index + 1;

            const moveDownObject = editingObject.parent.getChildAt(index);
            moveDownObject.order = index;
            proposedPositionInstance.editor.webSocketControllers.userPage.moveObjectUp(proposedPositionInstance.dbID, proposedPositionInstance.getFirstImportantParent().userPage._id);
        }

    }

    const imageToPage = (e) => {
        e.stopPropagation();
        proposedPositionInstance.objectInside.setFullSize2();
        proposedPositionInstance.editor.tools.init();
    }

    const imageToCenter = (e) => {
        e.stopPropagation();
        proposedPositionInstance.objectInside.center();
        proposedPositionInstance.editor.tools.init();
    }

    const handleRotateVertical = () => {
        let scaleX = proposedPositionInstance.scaleX;
        let scaleY = proposedPositionInstance.scaleY;
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
        .forEach(editingObject => {
            editingObject.setScale(scaleX, scaleY*-1);
            proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                editingObject.dbID,
                {
                    scaleX: editingObject.scaleX,
                    scaleY: editingObject.scaleY
                }
            );
        });
    }

    const handleRotateHorizontal = () => {
        let scaleX = proposedPositionInstance.scaleX;
        let scaleY = proposedPositionInstance.scaleY;
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
        .forEach(editingObject => {
            editingObject.setScale(scaleX*-1, scaleY);
            proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                editingObject.dbID,
                {
                    scaleX: editingObject.scaleX,
                    scaleY: editingObject.scaleY
                }
            );
        });
    }

    return (
        <>
            <div className="positions-wrapper">
                <div className="position-box">
                    <div className="position-buttons"> 
                    <LayerUpButton layerFunction={onLayerUpClick}/>
                    <LayerDownButton layerFunction={onLayerDownClick}/>
                    </div>
                    <span>przesuń</span>
                </div>
                <div className="position-box">
                    <div className='position-buttons'>
                        <HorizontalReflectButton rotateFunction={handleRotateHorizontal}/>  
                        <VerticalReflectButton rotateFunction={handleRotateVertical}/> 
                    </div>
                    <span>odbij</span>
                </div>
            </div>
                {/* <div className="position-box">
                    <div className='position-buttons'>
                        <CenterOnPageButton centerFunction = {imageToCenter}/>
                        <FullPageButton centerFunction = {imageToPage}/>
                    </div>
                    <span>Wycentruj</span>
                </div> */}
        </>
    );
};

export default PositionsWrapper;
