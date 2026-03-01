import React from "react";

export const LayerDownButton = ({ usedInModal = false, editor }) => {
    const handleclick = () => {
        console.log(editor)
    }
    return (
        <div className={`position-button layer-down-button ${usedInModal ? 'disable-actions' : ''}`} onClick={handleclick}> </div>
    );
};

