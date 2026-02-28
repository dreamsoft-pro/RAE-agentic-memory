import React from "react";

export const HorizontalReflectButton = ({rotateFunction}) => {
    return (
        <div className={`position-button horizontal-reflect-button`} onClick={rotateFunction}></div>
    );
};
