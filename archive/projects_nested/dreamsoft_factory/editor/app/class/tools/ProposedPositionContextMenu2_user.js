import ContextMenuTools from "../ContextMenuTools";
import {RANGE} from '../../Editor'
import React, {Component, createRef, useCallback, useEffect, useRef, useState} from 'react'
import {connect} from 'react-redux'
import {watch, unwatch} from 'melanke-watchjs'
import Toolbar from "./proposedPostionTools/Toolbar";
import ShadowTool from "./proposedPostionTools/ShadowTool";
import BorderTool from "./proposedPostionTools/BorderTool";
import {selectNone} from "../../redux/actions/tools";
import BackFrameTool from "./proposedPostionTools/BackFrameTool";
import EffectsTool from "./proposedPostionTools/EffectsTool";
import MaskTool from "./proposedPostionTools/MaskTool";
import {setProposedPosition} from "../../redux/actions/proposedPositionToolsActions";
import ProposedPositionBridge from "../../redux/ProposedPositionBridge";

class ProposedPositionContextMenu extends Component {
    constructor(props) {
        super(props);
        this.toolsContainer = createRef();

        this.state = {
            position: {
                left: 0,
                top: 0
            }
        }
    }

    componentDidMount() {
        console.log(`Tool for ${this.props.proposedPositionInstance.dbID} objectInside ${this.props.proposedPositionInstance.objectInside?this.props.proposedPositionInstance.objectInside.dbID:''}` )
        this._updateToolsBoxPosition()
        watch(this.props.proposedPositionInstance, ['x', 'y', 'rotation'], this.watchProposed, 0, true)
        this.props.setProposedPosition(this.props.proposedPositionInstance)
    }

    componentWillUnmount() {
        this.props.onUnmount()
        unwatch(this.props.proposedPositionInstance, ['x', 'y', 'rotation'], this.watchProposed)
        this.props.setProposedPosition(null)
    }

    watchProposed = (prop, action, newValue, oldValue) => {
        this._updateToolsBoxPosition()
    }

    _updateToolsBoxPosition() {
        const pos = this.props.proposedPositionInstance.getGlobalPosition()
        const bounds = this.props.proposedPositionInstance.getTransformedBounds()
        const stage = this.props.proposedPositionInstance.editor.getStage()

        const margin = this.props.advanced ? 16 : 8
        const toolsContainerHeight = this.props.advanced ? this.toolsContainer.current.offsetHeight / 2 + 12 : -this.toolsContainer.current.offsetHeight;

        this.setState({
            position: {
                top: pos[1] + bounds.height * stage.scaleY / 2 - toolsContainerHeight,
                left: pos[0] + bounds.width * stage.scaleX / 2 + margin
            }
        })
    }

    render() {
        return (
            this.props.proposedPositionInstance.objectInside && (
                <div
                    id="proposed-text-toolsbox"
                    className={"editor-bitmap-tools-box"}
                    ref={this.toolsContainer}
                    style={{
                        top: this.state.position.top,
                        left: this.state.position.left
                    }}
                >
                    <Toolbar proposedPositionInstance={this.props.proposedPositionInstance} advanced={this.props.advanced} ref={ref => {
                        this.toolbar = ref
                    }}/>
                    {/*<BackFrameTool proposedPositionInstance={this.props.proposedPositionInstance}/>*/}
                    {/*<BorderTool proposedPositionInstance={this.props.proposedPositionInstance}/>*/}
                    {/*<EffectsTool proposedPositionInstance={this.props.proposedPositionInstance}/>*/}
                    {/*<MaskTool proposedPositionInstance={this.props.proposedPositionInstance} />*/}
                    {/*<ShadowTool proposedPositionInstance={this.props.proposedPositionInstance}/>*/}
                    {/*<ProposedPositionBridge proposedPositionInstance={this.props.proposedPositionInstance}/>*/}
                </div>
            )
        )
    }
}

ProposedPositionContextMenu.propTypes = {}
const mapStateToProps = (state) => {
    return {}
}
const mapDispatchToProps = (dispatch) => {
    return {
        onUnmount: () => {
            dispatch(selectNone())
        },
        setProposedPosition: (pos) => {
            dispatch(setProposedPosition(pos))
        }
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(ProposedPositionContextMenu)
