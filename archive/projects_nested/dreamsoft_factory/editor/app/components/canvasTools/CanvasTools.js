import React from 'react'
import {useSelector} from "react-redux";
import ProposedPositionContextMenu from "../../class/tools/ProposedPositionContextMenu2_user";

const CanvasTools = () => {
    // this component might be usable when most of the editor part will be moved into React
    const { proposedPositionInstance } = useSelector(state => state.imagesReducer)
    return (
        <>
            {/*{images.active && proposedPositionInstance !== null && (*/}
            {/*    <ProposedPositionContextMenu proposedPositionInstance={proposedPositionInstance}/>*/}
            {/*)}*/}
        </>
    )
}

export default CanvasTools