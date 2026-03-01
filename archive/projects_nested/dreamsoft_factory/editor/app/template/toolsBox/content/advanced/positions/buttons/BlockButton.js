import React from 'react';

export const BlockButton = ({ usedInModal = false }) => {
    return (
        <div className={`position-button block-button ${usedInModal ? 'disable-actions' : ''}`}>
        </div>
    );
};
