import React from 'react';
import { LayerUpButton } from './buttons/LayerUpButton';
import { LayerDownButton } from './buttons/LayerDownButton';
import { VerticalReflectButton } from './buttons/VerticalReflectButton';
import { HorizontalReflectButton } from './buttons/HorizontalReflectButton';

const PositionsWrapper = ({ editor }) => {
    return (
        <div className="positions-wrapper">
            <div className="position-box">
                <div className="position-buttons"> 
                <LayerUpButton/>
                <LayerDownButton/>
                </div>
                <span>przesuń</span>
            </div>
            <div className="position-box">
                <div className='position-buttons'>
                    <VerticalReflectButton/>
                    <HorizontalReflectButton/>
                </div>
                <span>odbij</span>
            </div>
        </div>
    );
};

export default PositionsWrapper;
