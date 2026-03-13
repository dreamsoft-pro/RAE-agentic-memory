import {useSelector} from "react-redux";
import ToolOptionButton from "./ToolOptionButton";
import {store} from "../../../ReactSetup";
import React, {useEffect, useState} from "react";
import HeaderButton from "./HeaderButton";
import Slider from "../../../components/Slider";
import {setEditingImageEffects, setEditingImagePosition} from "../../../redux/reducers/images/selectedImage";
import ZoomIn from "../../../components/ZoomIn";
import {setActiveToolIndex} from "../../../redux/reducers/toolsbox/toolsBox";

// Tools for selected photo in header component (rotating, zooming in/out, positions and effects)
const SelectedImageTools = () => {
    const { selectedImage, proposedPositionInstance} = useSelector(state => state.selectedImageReducer);
    const { editorType } = useSelector(state => state.projectReducer);

    const [sliderProps, setSliderProps] = useState({
        step: 0.01,
        min: 1,
        max: 3,
        value: proposedPositionInstance.objectInside ? proposedPositionInstance.objectInside.scaleX : 1
    });

    const handleRotate = (e) => {
        e.stopPropagation();
        proposedPositionInstance.editor.webSocketControllers.proposedImage.rotateImageInside(
            proposedPositionInstance.editor.userProject.getCurrentView().Pages[0]._id,
            proposedPositionInstance.dbID
        );
    }

    const handleChangeZoom = (value) => {
        const currentScale = proposedPositionInstance.objectInside.scaleX;

        setSliderProps(prev => ({
            ...prev,
            value: value
        }));

        proposedPositionInstance.objectInside.setScale(value);

        proposedPositionInstance.objectInside.x *= value / currentScale;
        proposedPositionInstance.objectInside.y *= value / currentScale;
        proposedPositionInstance.objectInside.y += proposedPositionInstance.regY - proposedPositionInstance.regY * value / currentScale;
        proposedPositionInstance.objectInside.x += proposedPositionInstance.regX - proposedPositionInstance.regX * value / currentScale;

        if (proposedPositionInstance.objectInside.rotation % 180 === 0) {
            if (proposedPositionInstance.objectInside.x > proposedPositionInstance.objectInside.width / 2) {
                proposedPositionInstance.objectInside.x = proposedPositionInstance.objectInside.width / 2;
            } else if (proposedPositionInstance.objectInside.x + proposedPositionInstance.objectInside.width / 2 < proposedPositionInstance.trueWidth) {
                proposedPositionInstance.objectInside.x = proposedPositionInstance.trueWidth - proposedPositionInstance.objectInside.width / 2;
            }

            if (proposedPositionInstance.objectInside.y > proposedPositionInstance.objectInside.height / 2) {
                proposedPositionInstance.objectInside.y = proposedPositionInstance.objectInside.height / 2;
            } else if (proposedPositionInstance.objectInside.y + proposedPositionInstance.objectInside.height / 2 < proposedPositionInstance.trueHeight) {
                proposedPositionInstance.objectInside.y = proposedPositionInstance.trueHeight - proposedPositionInstance.objectInside.height / 2;
            }
        } else {
            if (proposedPositionInstance.objectInside.x > proposedPositionInstance.objectInside.height / 2) {
                proposedPositionInstance.objectInside.x = proposedPositionInstance.objectInside.height / 2;
            } else if (proposedPositionInstance.objectInside.x + proposedPositionInstance.objectInside.height / 2 < proposedPositionInstance.trueWidth) {
                proposedPositionInstance.objectInside.x = proposedPositionInstance.trueWidth - proposedPositionInstance.objectInside.height / 2;
            }

            if (proposedPositionInstance.objectInside.y > proposedPositionInstance.objectInside.width / 2) {
                proposedPositionInstance.objectInside.y = proposedPositionInstance.objectInside.width / 2;
            } else if (proposedPositionInstance.objectInside.y + proposedPositionInstance.objectInside.width / 2 < proposedPositionInstance.trueHeight) {
                proposedPositionInstance.objectInside.y = proposedPositionInstance.trueHeight - proposedPositionInstance.objectInside.width / 2;
            }
        }

        proposedPositionInstance.updateMask();
        proposedPositionInstance.calculateObjectInsideQuality(proposedPositionInstance.editor.getProductDPI());

        if (proposedPositionInstance.filterStack.length) {
            proposedPositionInstance.updateFilters();
        }

        proposedPositionInstance.redraw();
        reconfigureSlider();
    }
    
    const reconfigureSlider = () => {
        if (!proposedPositionInstance.objectInside)
            return;
        
        let minScale;

        if (proposedPositionInstance.objectInside.rotation % 180 !== 90) {
            minScale = proposedPositionInstance.width / proposedPositionInstance.objectInside.trueWidth;

            if (proposedPositionInstance.height > proposedPositionInstance.objectInside.trueHeight * minScale) {
                minScale = proposedPositionInstance.height / proposedPositionInstance.objectInside.trueHeight;
            }
        } else {
            minScale = proposedPositionInstance.height / proposedPositionInstance.objectInside.trueWidth;

            if (proposedPositionInstance.width > proposedPositionInstance.objectInside.trueHeight * minScale) {
                minScale = proposedPositionInstance.width / proposedPositionInstance.objectInside.trueHeight;
            }
        }

        setSliderProps(prev => ({
            ...prev,
            min: minScale,
            max: minScale + 2
        }));
    }

    const setTransform = () => {
        proposedPositionInstance.editor.webSocketControllers.editorBitmap.setTransform(
            proposedPositionInstance.objectInside.x,
            proposedPositionInstance.objectInside.y,
            proposedPositionInstance.objectInside.rotation,
            proposedPositionInstance.objectInside.scaleX,
            proposedPositionInstance.objectInside.scaleY,
            proposedPositionInstance.objectInside.dbID
        );
    }

    const handleOnClick = (value) => {
        handleChangeZoom(value);
        setTransform();
    }

    useEffect(() => {
        reconfigureSlider()
    }, []);

    return (
        <div className={'selected-image-container'}>
            <div className={'navigation-container white expanded'}>
                <ZoomIn
                    {...sliderProps}
                    handleOnClick={handleOnClick}
                />
                <HeaderButton
                    onClick={(e) => handleRotate(e)}
                    className={'no-border rotate'}
                />
                <Slider
                    {...sliderProps}
                    handleOnChange={handleChangeZoom}
                    handleOnStop={setTransform}
                />
            </div>
            <div className={"navigation-container gap expanded"}>
                {editorType === "advancedUser" && (
                    <ToolOptionButton
                        text={"Pozycje"}
                        isActive={selectedImage.position}
                        onClick={() => {
                            store.dispatch(setEditingImagePosition());
                            store.dispatch(setActiveToolIndex(0));
                        }}
                    />
                )}
                <ToolOptionButton
                    text={"Efekty"}
                    isActive={selectedImage.effects}
                    onClick={() => {
                        store.dispatch(setEditingImageEffects());
                        store.dispatch(setActiveToolIndex(0));
                    }}
                />
            </div>
        </div>
    )
}

export default SelectedImageTools