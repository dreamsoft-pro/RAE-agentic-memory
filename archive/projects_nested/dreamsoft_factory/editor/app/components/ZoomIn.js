import React from 'react'
import HeaderButton from "../template/topMenu/components/HeaderButton";

const ZoomIn = ({handleOnClick, ...props}) => {
    const handleZoomIn = () => {
        const { max, min, step, value } = props;
        const stepMultiplier = max - min / (1 / step);

        const newStep = step * stepMultiplier;
        const temp = value + newStep;

        let newValue = value;

        if (temp <= max) {
            newValue = temp;
        } else if (newStep + value > max) {
            newValue = max;
        }

        handleOnClick(newValue);
    }

    return (
        <HeaderButton
            className={'slider-zoom-in'}
            onClick={() => handleZoomIn()}
        />
    )
}

export default ZoomIn