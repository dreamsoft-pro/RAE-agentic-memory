import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Stepper from '../../../../components/Stepper';
import RangeOptions from './RangeOptions';
import Switch from "../../../../components/Switch";
import ColorTool from "../../../../components/canvasTools/ColorTool";

const FrameContent = ({ editor }) => {
    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);
    const { currentSelectedRange } = useSelector(state => state.range);
    const border = useSelector(state => state.proposedPositionBridge.border);

    const [borderWidth, setBorderWidth] = useState(proposedPositionInstance.borderWidth);

    const onSwitchChange = (displaySimpleBorder) => {
        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .forEach(editingObject => {
                if (displaySimpleBorder) {
                    editingObject.dropBorder();
                    editingObject.setBorderWidth(editingObject.borderWidth);
                    editingObject.updateSimpleBorder(true);
                } else {
                    editingObject.unDropBorder(true);
                }
                proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                    editingObject.dbID,
                    {
                        displaySimpleBorder,
                    }
                );
            });
    };

    const handleChangeColor = (newColorValue) => {
        const colorInHex = editor.rgb2hex(newColorValue);

        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .filter(o => o.objectInside)
            .forEach(editingObject => {
                editingObject.setBorderColor(colorInHex);

                proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                    editingObject.dbID,
                    {
                        borderColor: colorInHex
                    }
                );
            })
    }

    const changeWidth = (borderWidth, save) => {
        borderWidth = parseInt(borderWidth);
        setBorderWidth(borderWidth);
        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .filter(o => o.objectInside)
            .forEach(editingObject => {
                editingObject.setBorderWidth(borderWidth);
                editingObject.updateSimpleBorder();
                if (save) {
                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        {
                            borderWidth
                        }
                    );
                }
            });
    };

    const handleIncrease = () => {
        const newValue = borderWidth + 1;
        if (border) {
            onSwitchChange(true);
        }
        
        changeWidth(newValue);
    };

    const handleDecrease = () => {
        const newValue = Math.max(0, borderWidth - 1);

        changeWidth(newValue);

        if (border) {
            onSwitchChange(true);
        }

        if (newValue === 0) {
            onSwitchChange(false);
        }
    };

    const handleChange = (newValue) => {
        if (border && newValue > 0) {
            onSwitchChange(true);
        }
        changeWidth(newValue, true);
    };

    useEffect(() => {
        const savedThickness = proposedPositionInstance.borderWidth;

        if (savedThickness !== null) {
            const thickness = parseInt(savedThickness);

            changeWidth(thickness, true);
            // handleChangeColor(colorValue);
            setBorderWidth(thickness);
        }
    }, [proposedPositionInstance.borderWidth]);

    return (
        <>
            {/* <button onClick={setSolid}>Solid</button> */}
            <RangeOptions text='Opcje ramki dla zdjęcia:' />
            <div className='switch-container'>
                <Switch
                    label={{
                        close: "Wyłącz ramkę",
                        open: "Włącz ramkę"
                    }}
                    onChange={() => onSwitchChange(!border)}
                    checked={border > 0}
                />
            </div>
            <Stepper
                label="Grubość ramki"
                value={borderWidth}
                onIncrease={handleIncrease}
                onDecrease={handleDecrease}
                onChange={handleChange}
                min={0}
            />
            <ColorTool
                defaultColor={proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')[0]?.borderColor || 'rgba(0,0,0,1)'}
                label={"Kolor obramowania"}
                onChange={handleChangeColor}
                editor={editor}
            />
        </>
    );
};

export default FrameContent;