import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import Stepper from '../../../../components/Stepper';
import Switch from "../../../../components/Switch";
import RangeOptions from './RangeOptions';

const ShadowContent = () => {
    const { currentSelectedRange } = useSelector(state => state.range);
    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);
    const object = proposedPositionInstance;

    useEffect(() => {
        if (object) {
            const hasAnyShadowValue = object.shadowBlur > 0 || object.shadowOffsetX !== 0 || object.shadowOffsetY !== 0;
            onSwitchChange(hasAnyShadowValue);
        }
    }, [object]);

    const [shadowBlur, setShadowBlur] = useState(object?.shadowBlur || 0);
    const [shadowOffsetX, setShadowOffsetX] = useState(object?.shadowOffsetX || 0);
    const [shadowOffsetY, setShadowOffsetY] = useState(object?.shadowOffsetY || 0);
    const [isDropShadow, setIsDropShadow] = useState(object?.dropShadow);

    const onSwitchChange = (checked) => {
        if (shadowBlur === 0 && shadowOffsetX === 0 && shadowOffsetY === 0 && checked) {
            return;
        }

        setIsDropShadow(checked);
        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .forEach(editingObject => {
                if (checked){
                    editingObject.dropShadowAdd();
                } else {
                    editingObject.unDropShadow();
                }
                proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                    editingObject.dbID,
                    { 
                        dropShadow: checked,
                    }
                );
            });
    };

    const changeShadow = (propertyName, value, save) => {
        const setterName = {
            shadowBlur: 'setShadowBlur',
            shadowColor: 'setShadowColor',
            shadowOffsetX: 'setShadowOffsetX',
            shadowOffsetY: 'setShadowOffsetY',
            horizontalPadding: 'setHorizontalPadding',
            verticalPadding: 'setVerticalPadding'
        }[propertyName];

        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .forEach(editingObject => {
                editingObject[setterName](value);
                editingObject.updateShadow();
                if (save) {
                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        {
                            [propertyName]: value,
                        }
                    );
                }
            });
    };

    const handleStepperChange = (property, value) => {
        let validatedValue = value;
        if (property === 'shadowBlur') {
            validatedValue = Math.min(Math.max(value, 0), 50);
        } else {
            validatedValue = Math.min(Math.max(value, -50), 50);
        }

        let newValues = {
            shadowBlur: property === 'shadowBlur' ? validatedValue : shadowBlur,
            shadowOffsetX: property === 'shadowOffsetX' ? validatedValue : shadowOffsetX,
            shadowOffsetY: property === 'shadowOffsetY' ? validatedValue : shadowOffsetY
        };
    
        const allValuesZero = Object.values(newValues).every(val => val === 0);
        if (allValuesZero) {
            setIsDropShadow(false);
            onSwitchChange(false);
        } else if (!isDropShadow) {
            setIsDropShadow(true);
            onSwitchChange(true);
        }
    
        changeShadow(property, validatedValue, true);

        switch(property) {
            case 'shadowBlur':
                setShadowBlur(validatedValue);
                break;
            case 'shadowOffsetX':
                setShadowOffsetX(validatedValue);
                break;
            case 'shadowOffsetY':
                setShadowOffsetY(validatedValue);
                break;
        }
    };

    return (
        <>
            <RangeOptions text='Opcje cienia dla zdjęcia:' />
                <div className='switch-container'>
                    <Switch
                        label={{
                            close: "Wyłącz cień",
                            open: "Włącz cień"
                        }}
                        onChange={() => onSwitchChange(!isDropShadow)}
                        checked={isDropShadow}
                    />
                </div>
                <div className={'scroll-y-container'}>
                    <div className='stepper-shadow-container'>
                        <Stepper
                            label="Rozmycie cienia"
                            value={shadowBlur}
                            onChange={(value) => handleStepperChange('shadowBlur', value)}
                            onIncrease={() => handleStepperChange('shadowBlur', shadowBlur + 1)}
                            onDecrease={() => handleStepperChange('shadowBlur', shadowBlur - 1)}
                            min={0}
                        />
                        <Stepper
                            label="Przesunięcie X"
                            value={shadowOffsetX}
                            onChange={(value) => handleStepperChange('shadowOffsetX', value)}
                            onIncrease={() => handleStepperChange('shadowOffsetX', shadowOffsetX + 1)}
                            onDecrease={() => handleStepperChange('shadowOffsetX', shadowOffsetX - 1)}
                            min={-50}
                            max={50}
                        />
                        <Stepper
                            label="Przesunięcie Y"
                            value={shadowOffsetY}
                            onChange={(value) => handleStepperChange('shadowOffsetY', value)}
                            onIncrease={() => handleStepperChange('shadowOffsetY', shadowOffsetY + 1)}
                            onDecrease={() => handleStepperChange('shadowOffsetY', shadowOffsetY - 1)}
                            min={-50}
                            max={50}
                        />
                    </div>
            </div>
        </>
    );
};

export default ShadowContent;