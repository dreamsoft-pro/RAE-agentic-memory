import React, {useEffect, useRef} from 'react'
import ColorPicker from "react-best-gradient-color-picker";
import {useSelector} from "react-redux";
import {store} from "../../ReactSetup";
import {
    addNewColorPreset, setColorPickerOnChangeHandler, setColorPickerValue,
    setColorPickerVisibility
} from "../../redux/reducers/colorPicker/colorPickerReducer";

const ColorPickerModal = () => {
    const {
        isPickerVisible,
        colorValue,
        colorPickerOnChangeHandler,
        canCloseColorPickerModal,
    } = useSelector(state => state.colorPickerReducer);

    const containerRef = useRef(null);
    const colorPickerRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (canCloseColorPickerModal && isPickerVisible && containerRef.current && !containerRef.current.contains(event.target)) {
                store.dispatch(setColorPickerVisibility(false));
                store.dispatch(setColorPickerValue(null));
                store.dispatch(setColorPickerOnChangeHandler(() => {}));
            }
        }

        const handleAddNewPreset = (event) => {
            if (colorPickerRef.current && colorPickerRef.current.contains(event.target)) {
                store.dispatch(addNewColorPreset(colorValue));
            }
        }

        document.addEventListener('mousedown', handleClickOutside);
        document.addEventListener('mouseup', handleAddNewPreset);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
            document.removeEventListener('mouseup', handleAddNewPreset);
        }
    }, [colorValue, canCloseColorPickerModal, isPickerVisible]);

    const handleOnChange = (newColorValue) => {
        store.dispatch(setColorPickerValue(newColorValue));
        colorPickerOnChangeHandler(newColorValue);
    }

    return (
        <div
            ref={containerRef}
            className={`color-picker-modal ${isPickerVisible ? '' : 'hidden'}`}
        >
            <div
                ref={colorPickerRef}
                className={'color-picker-container'}
            >
                <ColorPicker
                    value={colorValue}
                    onChange={handleOnChange}
                    hideColorTypeBtns
                    hideEyeDrop
                    hidePresets
                    disableDarkMode
                />
            </div>
        </div>
    )
}

export default ColorPickerModal