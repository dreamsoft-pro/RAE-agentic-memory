import React, {Component} from 'react'

export default class LayerDownTool extends Component {

    render() {
        return (
            <button className={"bitmap-tool-button layer-down"} id={"layerDownButton"} onClick={this.props.onClick}/>
        )
    }
}
