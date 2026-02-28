import React, {Component} from 'react'

export default class DeleteTool extends Component {

    render() {
        return (
            <button
                onClick={this.props.onClick}
                className={"bitmap-tool-button remove"} id="removeImage"
            />
        )
    }
}
