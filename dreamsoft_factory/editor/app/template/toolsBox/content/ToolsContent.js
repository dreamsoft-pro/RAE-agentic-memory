import React from "react";
import BlankContent from "./BlankContent";
import toolsList from "../ToolsList";
import {useSelector} from "react-redux";
import ColorPickerModal from "../../modals/ColorPickerModal";

export const ToolsContent = ({editor, type}) => {
    const activeIndex = useSelector(state => state.toolReducer.activeToolIndex);

    return (
       <div id={"toolsContent"}>
           {toolsList.map((tool, index) => (
               <tool.toolContent key={index} editor={editor} type={type} className={activeIndex === index ? "active-tool-content" : ""} />
           ))}
           <BlankContent/>
           <ColorPickerModal />
       </div>
    )
}