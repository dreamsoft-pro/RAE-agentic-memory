import React from "react";

export const VerticalReflectButton = ({rotateFunction}) => {
    return (
        <div className={`position-button vertical-reflect-button`} onClick={rotateFunction}></div>
    );
};
