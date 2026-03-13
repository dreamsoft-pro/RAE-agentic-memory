import {useSelector} from "react-redux";
import React from "react";
import Selector from "./Selector";
import {changeFontSize} from "../../redux/actions/textTools";
import {store} from "../../ReactSetup";

const FontSizeSelector = () => {
    const { fontSize, fontSizes } = useSelector(state => state.text2Bridge)

    const renderItem = (item) => {
        return (
            <span className={'item-name'}>{item.value}</span>
        )
    }

    const handleOnChange = (item) => {
        store.dispatch(changeFontSize(item.value));
    }

    return (
        <Selector
            renderItem={renderItem}
            elements={fontSizes.map(size => ({value: size}))}
            selected={fontSizes.indexOf(fontSize)}
            onChange={handleOnChange}
            gray
         />
    )
}

export default FontSizeSelector;