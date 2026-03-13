import React from "react";

export const LayerUpButton = ({ layerFunction }) => {
    return (
        <div className={`position-button layer-up-button`} onClick={layerFunction}></div>
    );
};
