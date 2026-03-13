import React from 'react';

export const ConnectButton = ({ usedInModal = false }) => {
    return (
        <div className={`connect-dimensions ${usedInModal ? 'disable-actions' : ''}`}>
        </div>
    );
};
