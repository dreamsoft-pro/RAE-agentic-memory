import React from 'react';
import { BlockButton } from './buttons/BlockButton';

const BlockWrapper = () => {
    return (
        <div className="block-wrapper">
            <BlockButton/>
            <span>Zablokuj</span>
        </div>
    );
};

export default BlockWrapper;
