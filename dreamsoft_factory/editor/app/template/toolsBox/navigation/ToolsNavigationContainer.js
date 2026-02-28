import React from 'react'
import ToolButtonContainer from "./ToolButtonContainer";
import toolsList from "../ToolsList";
import {useSelector} from "react-redux";

const ToolsNavigationContainer = () => {
    const {editorType} = useSelector(state => state.projectReducer)

    return (
        <div id={"toolsContainer"}>
            {toolsList.filter(tool => editorType === "user" ? tool.type === 'simple' : true).map((tool, index) => (
                <ToolButtonContainer
                    key={index}
                    index={index}
                    className={`${tool.toolButton.className}`}
                    text={tool.toolButton.text}
                />
            ))}
        </div>

    )
}

export default ToolsNavigationContainer