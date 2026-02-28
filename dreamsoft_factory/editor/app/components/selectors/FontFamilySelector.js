import {store} from "../../ReactSetup";
import {changeFontFamily} from "../../redux/actions/textTools";
import React, {useCallback, useEffect, useState} from "react";
import Selector from "./Selector";

const FontFamilySelector = ({editor}) => {
    let { currentFonts } = editor.fonts

    const [fonts] = useState(
        Object.entries(currentFonts).map(([key, value]) => ({
            value: key,
            ...value
        }))
    );

    const handleOnChange = (item) => {
        store.dispatch(changeFontFamily(item.name));
    }

    const renderItem = (item) => {
        return (
            <>
                <img
                    alt={`Podgląd czcionki ${item.value}`}
                    src={EDITOR_ENV.staticUrl + item.miniature}
                    className={'font-preview'}
                />
                <span className={'item-name'}>{item.value}</span>
            </>
        )
    }

    return (
        <Selector
            gray
            selected={0}
            elements={fonts}
            renderItem={renderItem}
            onChange={handleOnChange}
        />
    )
}
export default FontFamilySelector;