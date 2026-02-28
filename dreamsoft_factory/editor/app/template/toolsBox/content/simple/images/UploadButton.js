import React, {Component} from 'react';
import FileUploader from "./FileUploader";

export default class UploadButton extends Component {
    constructor(props) {
        super(props);
        this.usedInModal = props.usedInModal || false;
        this.uploadFunc = this.props.uploadFunc;
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        $('#images-uploader').click();
    }


    render() {


        return (
            <button
                className={`add-photos main-tool-button ${this.usedInModal ? "disable-actions" : ""}`}
                id="innerUploadContainer"
                onClick={() => this.handleClick()}
            >
                Dodaj obrazy
                {!this.usedInModal && (
                    <>
                        <div
                            id="projectImageVisibleUploader"
                            className="absolutePos"
                        >
                        </div>
                        <FileUploader uploadFunc={this.uploadFunc}/>
                    </>
                )}
            </button>
        );
    }
}