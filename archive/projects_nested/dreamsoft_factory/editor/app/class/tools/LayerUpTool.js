import React, {Component} from 'react'

export default class LayerUpTool extends Component {

    render() {
        return (
            <button className={"bitmap-tool-button layer-up"} id={"layerUpButton"} onClick={this.props.onClick}/>
        )

    }
}
