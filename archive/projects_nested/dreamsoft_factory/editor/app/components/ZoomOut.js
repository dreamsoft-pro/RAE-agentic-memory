import React from 'react'
import HeaderButton from "../template/topMenu/components/HeaderButton";

const ZoomOut = ({handleOnClick, ...props}) => {
    const handleZoomOut = () => {
        const { min, max, value, step } = props;
        const stepMultiplier = max - min / (1 / step);

        const newStep = step * stepMultiplier;
        const temp = value - newStep;

        let newValue = value;

        if (temp >= min) {
            newValue = temp;
        } else if (value - newStep < min) {
            newValue = min;
        }

        handleOnClick(newValue);
    }

    return (
        <HeaderButton
            className={'slider-zoom-out'}
            onClick={() => handleZoomOut()}
        />
    )
}

export default ZoomOut