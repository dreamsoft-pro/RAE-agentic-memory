import React, {Component} from 'react';

class FileUploader extends Component {
    constructor(props) {
        super(props);
    }

    handleFileChange(e) {
        const files = e.target.files;
        this.props.uploadFunc(files);
    }

    render() {
        return (
            <input
                id={"images-uploader"}
                type="file"
                multiple
                accept={'image/*'}
                className="inputHidden absolutePos"
                onChange={(e) => this.handleFileChange(e)}
            />
        );
    }
}

export default FileUploader;