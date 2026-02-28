import React, {useEffect, useRef, useState} from 'react'
import RangeOptions from "./RangeOptions";
import Switch from "../../../../components/Switch";
import {safeImage} from "../../../../utils";
import {useSelector} from "react-redux";
import Slider from "../../../../components/Slider";
import Stepper from "../../../../components/Stepper";

export const effects = {
    'SEPIA': () => new createjs.ColorMatrixFilter([
        0.39, 0.77, 0.19, 0, 0,
        0.35, 0.68, 0.17, 0, 0,
        0.27, 0.53, 0.13, 0, 0,
        0, 0, 0, 1, 0
    ]),
    'BW': () => new createjs.ColorMatrixFilter([
        0.30, 0.30, 0.30, 0, 0,
        0.30, 0.30, 0.30, 0, 0,
        0.30, 0.30, 0.30, 0, 0,
        0, 0, 0, 1, 0
    ]),
    'NEGATIVE': () => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustHue(-200)
    ),

    'BRIGHTNESS': (value = 50) => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustBrightness(value)
    ),

    'CONTRAST': (value = 50) => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustContrast(value)
    ),

    'SATURATION': (value = 50) => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustSaturation(value)
    ),

    'HUE': (value = 180) => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustHue(value)
    ),

    'INVERT': () => new createjs.ColorMatrixFilter([
        -1, 0, 0, 0, 255,
        0, -1, 0, 0, 255,
        0, 0, -1, 0, 255,
        0, 0, 0, 1, 0
    ]),

    'GRAYSCALE': (value = 1) => new createjs.ColorMatrixFilter(
        new createjs.ColorMatrix().adjustSaturation(-value)
    ),

    'COLORIZE': (red = 255, green = 0, blue = 0, intensity = 1) => new createjs.ColorMatrixFilter([
        intensity, 0, 0, 0, red * (1 - intensity),
        0, intensity, 0, 0, green * (1 - intensity),
        0, 0, intensity, 0, blue * (1 - intensity),
        0, 0, 0, 1, 0
    ])
};

const effectDefault = effects[0];

const ImageEffects = () => {
    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);
    const { currentSelectedRange } = useSelector(state => state.range);

    const [effectsStatus, setEffectsStatus] = useState(true);
    const [effectsList, setEffectsList] = useState(['', ...Object.keys(effects)]);

    const handleSwitchChange = () => {
        setEffectsStatus((prev) => {
            changeEffect(!prev ? effectDefault : '');
            setEffectsStatus(!prev);
        })
    }

    const handleEffectClick = (effectName) => {
        if (effectsStatus) {
            changeEffect(effectName);
        }
    }

    const changeEffect = (effectName) => {
        proposedPositionInstance.editor.getEditableObjectsByType(currentSelectedRange, 'ProposedPosition')
            .forEach(editingObject => {
                    editingObject.setEffect(effectName, true);

                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        { effectName },
                        proposedPositionInstance.editor.userPage._id
                    );
                }
            );
    }

    return (
        <>
            <RangeOptions text={'Opcje efektów dla zdjęcia'}/>
            <Switch
                id={'enableImageEffects'}
                checked={effectsStatus}
                onChange={() => handleSwitchChange()}
                label={{
                    close: "Wyłącz efekty",
                    open: "Włącz efekty"
                }}
            />
            <ImageOpacityChanger proposedPositionInstance={proposedPositionInstance}/>
            <div className={'scroll-y-container'}>
                <div className={'grid-container three-columns'}>
                    {effectsList.map((effect, index) => (
                        <div
                            key={index}
                            className={'photo-item'}
                            onClick={() => handleEffectClick(effect)}
                        >
                            <ItemRenderer
                                proposedPositionInstance={proposedPositionInstance.objectInside.projectImage}
                                type={effect}
                            />
                        </div>

                    ))}
                </div>
            </div>
        </>
    )
}

const ImageOpacityChanger = ({proposedPositionInstance}) => {
    const [sliderProperties, setSliderProperties] = useState({
        min: 0,
        max: 1,
        step: 0.01,
        value: proposedPositionInstance.objectInside.alpha || 1
    });

    const round = (value) => {
        return parseFloat(value.toFixed(10))
    }

    const setImageOpacity = (value) => {
        setSliderProperties(prev => ({
            ...prev,
            value: value
        }))

        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
            .forEach(editingObject => {
                    editingObject.setOpacity(value, true);

                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        { alpha: value },
                        proposedPositionInstance.editor.userPage._id
                    );
                }
            );
    }

    const stepperProperties = {
        onDecrease: () => {
            if (sliderProperties.value > sliderProperties.min)
                setImageOpacity(round(sliderProperties.value - sliderProperties.step))
        },
        onIncrease: () => {
            if (sliderProperties.value < sliderProperties.max)
                setImageOpacity(round(sliderProperties.value + sliderProperties.step))
        },
        onChange: (value) => {
            setImageOpacity(round(value));
        },
        label: "Przezroczystość",
        min: sliderProperties.min,
        max: sliderProperties.max,
        value: sliderProperties.value,
    }

    const handleSliderChange = (value) => {
        setImageOpacity(value)
    }

    return (
        <div className={"flex-col gap-4"}>
            <Slider
                {...sliderProperties}
                handleOnChange={handleSliderChange}
            />
            <Stepper
                {...stepperProperties}
            />
        </div>
    )
}

const ItemRenderer = ({type, proposedPositionInstance}) => {
    const canvasRef = useRef();

    const applyFilters = (bmp) => {
        if (type !== '') {
            bmp.filters = [effects[type]()]
        }
    }

    useEffect(() => {
        const stage = new createjs.Stage(canvasRef.current);
        const img = safeImage()

        img.addEventListener('load', () => {
            const bmp = new createjs.Bitmap(img)
            stage.addChild(bmp)

            bmp.cache(0, 0, img.width, img.height)
            const h = 86
            bmp.scale = h / img.height * 2//TODO why must be multiplier
            canvasRef.current.width = bmp.scale * img.width

            applyFilters(bmp)

            bmp.updateCache()
            stage.update()
        })

        let src = proposedPositionInstance.thumbnail

        if (src.indexOf('http') !== 0) {
            src=`${EDITOR_ENV.staticUrl}${src}`
        }
        img.src = src

    }, []);

    return <canvas ref={canvasRef}></canvas>
}

export default ImageEffects