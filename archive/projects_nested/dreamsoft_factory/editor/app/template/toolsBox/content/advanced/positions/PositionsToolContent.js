import React from 'react';
import MainButton from './buttons/MainButton';
import DimensionsWrapper from './DimensionsWrapper';
import AngleWrapper from './AngleWrapper';
import PositionsWrapper from './PositionsWrapper';
import BlockWrapper from './BlockWrapper';

const PositionsToolContent = ({editor, className = "" }) => {
    return (
        <div id="positions-container-tool" className={className}>
            <MainButton />
            <div className="tools-wrapper">
                <DimensionsWrapper />
                <AngleWrapper />
                <PositionsWrapper editor={editor}/>
                <BlockWrapper />
            </div>
        </div>
    );
};

export default PositionsToolContent;
