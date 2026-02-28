import React from 'react';
import ToolButton from "../navigation/ToolButton";
import ProductAttributes from '../../ProductAttributes';

const AttributesButtonsList = {
    Component: ({...props}) => <ToolButton className={"attributes"} {...props} />,
    title: "Cechy Produktu",
    description: "W tym narzędziu możesz dostosować atrybuty produktu.",
    Components: {}
}

export default AttributesButtonsList;
