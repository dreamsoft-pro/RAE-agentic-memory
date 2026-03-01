import React from 'react'
import MainButton from './MainButton'

const LayersToolContent = ({className = ""}) => {
    return (
        <div id="layers-container-tool" className={className}>
            <MainButton/>
            <div id="layersContent">
                <div id="layers-main-content">
                    <div id="editorLayers"></div>
                </div>
            </div>
        </div>
    )
}

export default LayersToolContent