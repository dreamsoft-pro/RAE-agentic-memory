import React from 'react';

export const ConnectButton = ({ isConnected, toggleConnect }) => {
    return (
        <div className={`connect-dimensions ${isConnected ? 'active' : ''}`}  onClick={toggleConnect}>
        </div>
    );
};
