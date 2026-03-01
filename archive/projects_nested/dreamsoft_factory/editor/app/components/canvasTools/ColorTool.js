import React, {useEffect, useState} from 'react';
import {useColorPicker} from "react-best-gradient-color-picker";
import {
    setColorPickerVisibility,
    setColorPickerOnChangeHandler, setCanCloseColorPickerModal, setColorPickerValue
} from "../../redux/reducers/colorPicker/colorPickerReducer";
import {useSelector} from "react-redux";
import {store} from "../../ReactSetup";
import {Bitmap} from "../../class/EditorBitmap";

const ColorTool = ({editor, onChange, label, defaultColor}) => {
    const { colorValue, defaultPresets, previousPresets } = useSelector(state => state.colorPickerReducer)
    const colorPickerComponent = useColorPicker(colorValue, onChange);

    const showColorPicker = () => {
        store.dispatch(setColorPickerVisibility(true));
        store.dispatch(setColorPickerOnChangeHandler(onChange));
    };

    const handlePresetClick = (presetColorValue) => {
        showColorPicker();
        onChange(presetColorValue);
        store.dispatch(setColorPickerValue(presetColorValue));
    }

    const disableToCloseModal = () => {
        store.dispatch(setCanCloseColorPickerModal(false));
    }

    const enableToCloseModal = () => {
        store.dispatch(setCanCloseColorPickerModal(true));
    }

    useEffect(() => {
        store.dispatch(setColorPickerValue(defaultColor));
    }, [])

    return (
        <>
            <div className={'color-picker-tool-container'}>
                <span>{label}</span>
                <ColorUnderPixelButton
                    showColorPicker={showColorPicker}
                    editor={editor}
                />
                <ColorPickerButton
                    currentColor={colorValue}
                    showColorPicker={showColorPicker}
                    onMouseEnter={() => disableToCloseModal()}
                    onMouseLeave={() => enableToCloseModal()}
                />
            </div>
            <div className={'grid-container six-columns'}>
                {defaultPresets.map((preset, index) => (
                    <div
                        key={index}
                        onClick={() => handlePresetClick(preset)}
                        onMouseEnter={() => disableToCloseModal()}
                        onMouseLeave={() => enableToCloseModal()}
                        className={`color-picker-preset ${colorValue === preset ? "active" : ""}`}
                        style={{
                            backgroundColor: preset
                        }}
                    />
                ))}
                {previousPresets.map((preset, index) => (
                    <div
                        key={index}
                        onClick={() => handlePresetClick(preset)}
                        onMouseEnter={() => disableToCloseModal()}
                        onMouseLeave={() => enableToCloseModal()}
                        className={`color-picker-preset ${colorValue === preset ? "active" : ""}`}
                        style={{
                            backgroundColor: preset
                        }}
                    />
                ))}
            </div>
        </>
    )
}

const ColorUnderPixelButton = ({ editor, showColorPicker }) => {
    const [isEnabled, setIsEnabled] = useState(false)

    const handleClick = () => {
        setIsEnabled(!isEnabled);
        editor.isGettingColorFromBitmap = !isEnabled;
    }

    const handleMouseOut = () => {
        editor.getStage().canvas.style.cursor = 'default';
    }

    const getColorUnderMousePosition = (stageX, stageY, offsetX, offsetY) => {
        const pos = editor.stage.getMousePosition(stageX, stageY);

        const bitmapsUnderPoint = editor.getStage()
            .getObjectsUnderPoint(pos[0], pos[1], [])
            .filter(element => element instanceof Bitmap);

        if (!bitmapsUnderPoint.length) {
            return { color: null };
        }

        const ctx = editor.getStage().canvas.getContext('2d')
        const imageData = ctx.getImageData(stageX + offsetX, stageY + offsetY, 1, 1).data;
        const mouseOffset = 5;

        return {
            color: imageData,
            x: pos[0] + mouseOffset + offsetX * 6,
            y: pos[1] + mouseOffset + offsetY * 6
        };
    };


    const initColorInfoContainer = () => {
        const container = new createjs.Container()
        editor.getStage().addChild(container);

        const colorBox = new createjs.Shape();
        container.addChild(colorBox);

        // const colorText = new createjs.Text('', '6px Arial', '#000');
        // colorText.x = 2;
        // colorText.y = 2;
        //
        // container.addChild(colorText);

        return { parent: container, colorBox }
    }

    const handleStageMouseMove = (event, containers) => {
        editor.getStage().canvas.style.cursor = 'crosshair';

        const { stageX, stageY } = event

        for (let i = 0; i < containers.length; i++) {
            for (let j = 0; j < containers[i].length; j++) {
                const { color, x, y } = getColorUnderMousePosition(stageX, stageY, i, j);

                if (color === null)
                    return;

                // creating small container that shows what color we've got under mouse current position
                const [r, g, b] = color;

                const hex = `#${((1 << 24) | (r << 16) | (g << 8) | b)
                    .toString(16)
                    .slice(1)}`;

                containers[i][j].colorBox.graphics.clear().beginFill(hex).drawRect(0,0,6,6);

                containers[i][j].parent.x = x
                containers[i][j].parent.y = y
            }
        }
        editor.getStage().update();
    }

    const handleGetColorFromBitmap = (event) => {
        const { stageX, stageY } = event;
        const {color, x, y} = getColorUnderMousePosition(stageX, stageY);

        if (color === null)
            return;
    }

    useEffect(() => {
        let containers = [];
        for (let i = 0; i < 5; i++) {
            let array = [];

            for (let j = 0; j < 5; j++) {
                array.push(initColorInfoContainer())
            }

            containers.push(array)
        }

        if (isEnabled) {
            editor.getStage().addEventListener('mouseout', handleMouseOut);
            editor.getStage().addEventListener('click', handleGetColorFromBitmap)
            editor.getStage().addEventListener('stagemousemove', (event) => handleStageMouseMove(event, containers))
        }

        return () => {
            editor.getStage().removeEventListener('mouseout', handleMouseOut);
            editor.getStage().removeEventListener('click', handleGetColorFromBitmap);
            editor.getStage().removeEventListener('stagemousemove', (event) => handleStageMouseMove(event, containers))
        }
    }, [isEnabled]);

    return (
        <button
            className={`get-color-under-pixel-button ${isEnabled ? "active" : ""}`}
            onClick={() => handleClick()}
        />
    )
}

const ColorPickerButton = ({currentColor, showColorPicker, ...props}) => {
    return (
        <div
            onClick={() => showColorPicker()}
            className={'color-picker-button-container'}
            {...props}
        >
            <div
                className={'color-picker-button'}
                style={{
                    backgroundColor: currentColor
                }}
            />
        </div>
    )
}

export default ColorTool