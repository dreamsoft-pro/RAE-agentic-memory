import {useSelector} from "react-redux";
import ToolOptionButton from "./ToolOptionButton";
import {store} from "../../../ReactSetup";
import {setEditingTextEffects} from "../../../redux/reducers/project/project";
import React from "react";
import FontSizeButton from "./FontSizeButton";
import HeaderButton from "./HeaderButton";
import FontFamilySelector from "../../../components/selectors/FontFamilySelector";
import FontSizeSelector from "../../../components/selectors/FontSizeSelector";

// Tools for selected text in header component (zooming in, changing font type, font size, effects)
const SelectedTextTools = ({editor}) => {
    const { text } = useSelector(state => state.projectReducer);

    return (
        <div className={'selected-image-container'}>
            <div className={'navigation-container white expanded'}>
                <HeaderButton className={'no-border slider-zoom-in'}/>
                <FontFamilySelector editor={editor} />
                <FontSizeSelector />
                <FontSizeButton type={'increment'}/>
                <FontSizeButton type={'decrement'}/>
            </div>
            <div className={"navigation-container expanded"}>
                <ToolOptionButton
                    text={"Efekty"}
                    isActive={text.effects}
                    onClick={() => store.dispatch(setEditingTextEffects())}
                />
            </div>
        </div>
    )
}

export default SelectedTextTools