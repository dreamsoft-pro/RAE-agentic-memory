import React from "react";
import ToolButton from "../ToolButton";
import ToolHelper from "../ToolHelper";

/**
 * Generuje przyciski do otworzenia narzędzia do obrazków
 */
export default class AttributesToolContainer extends React.Component {
    render() {
        return (
            <>
                <ToolButton className={"attributes"} id={"attributes-container-tool_button"} dataContent={"attributesContent"}/>
                <ToolHelper>Tutaj edytować atrybuty</ToolHelper>
            </>

        )

    }
}