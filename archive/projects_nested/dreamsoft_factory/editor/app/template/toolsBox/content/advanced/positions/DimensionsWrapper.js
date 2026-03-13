import React from 'react';
import { ConnectButton } from './buttons/ConnectButton';

const DimensionsWrapper = () => {
    return (
        <div className="dimensions-wrapper">
            <div className="width-height-container">
                <div className="height-box">
                    <span>W:</span>
                    <input type="number" className="height-input" />
                </div>
                <div className="width-box">
                    <span>S:</span>
                    <input type="number" className="width-input" />
                </div>
                <ConnectButton/>
            </div>
            <div className="width-height-container">
                <div className="height-box">
                    <span>X:</span>
                    <input type="number" className="height-input" />
                </div>
                <div className="width-box">
                    <span>Y:</span>
                    <input type="number" className="width-input" />
                </div>
            </div>
        </div>
    );
};

export default DimensionsWrapper;
