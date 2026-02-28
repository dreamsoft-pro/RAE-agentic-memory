import React from "react";

export const VerticalReflectButton = ({ usedInModal = false }) => {
    return (
        <div className={`position-button vertical-reflect-button ${usedInModal ? 'disable-actions' : ''}`}></div>
    );
};
