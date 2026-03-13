import React from "react";

export const CenterOnPageButton = ({centerFunction}) => {
    return (
        <div className={`position-button center-on-page-button`} onClick={centerFunction}></div>
    );
};
