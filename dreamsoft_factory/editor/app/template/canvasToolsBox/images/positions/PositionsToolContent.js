import React from 'react'
import DimensionsWrapper from './DimensionsWrapper'
import AngleWrapper from './AngleWrapper'
import PositionsWrapper from './PositionsWrapper'
import BlockWrapper from './BlockWrapper'

const PositionToolContent = () => {
    return (
        <>
            <div className="tools-wrapper">
                <DimensionsWrapper />
                <AngleWrapper />
                <PositionsWrapper />
                <BlockWrapper />
            </div>
        </>
    )
}

export default PositionToolContent