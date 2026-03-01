import React from 'react';

export const AngleButton = ({ usedInModal = false }) => {
    return (
        <div className={`position-button angle-button ${usedInModal ? 'disable-actions' : ''}`}>
        </div>
    );
};
