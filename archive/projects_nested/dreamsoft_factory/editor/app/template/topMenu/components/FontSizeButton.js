import React from 'react'
import {useSelector} from "react-redux";
import {store} from "../../../ReactSetup";
import {changeFontSize} from "../../../redux/actions/textTools";

const FontSizeButton = ({type}) => {
    const {fontSizes, fontSize, fontSizesProps} = useSelector(store => store.text2Bridge);
    const {step} = fontSizesProps;

    const handleClick = () => {
        if (type === 'increment' && fontSize + step <= fontSizes[fontSizes.length - 1]) {
            console.log(fontSize + step)
            store.dispatch(changeFontSize( fontSize + step))
        } else if (type === 'decrement' && fontSize - step >= fontSizes[0]) {
            store.dispatch(changeFontSize( fontSize - step))
        }
    }
    return (
        <button
            onClick={() => handleClick()}
            className={`hover control-font-size-button ${type}`}
        />
    )
}

export default FontSizeButton