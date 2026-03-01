import React from "react";

export const LayerUpButton = ({ usedInModal = false }) => {
    return (
        <div className={`position-button layer-up-button ${usedInModal ? 'disable-actions' : ''}`}></div>
    );
};
