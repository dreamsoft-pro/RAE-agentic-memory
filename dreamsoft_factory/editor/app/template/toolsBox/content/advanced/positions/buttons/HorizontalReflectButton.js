import React from "react";

export const HorizontalReflectButton = ({ usedInModal = false }) => {
    return (
        <div className={`position-button horizontal-reflect-button ${usedInModal ? 'disable-actions' : ''}`}></div>
    );
};
