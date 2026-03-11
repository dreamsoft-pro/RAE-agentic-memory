import React from 'react';
import { Modal } from 'react-bootstrap'; // Assuming bootstrap for modal implementation
import api from '@/lib/api';

class PrintShopUploader extends React.Component {
    state = {
        showModal: false,
        uploader: null,
        destination: ''
    };

    componentDidMount() {
        this.setState({ showModal: true });
    }

    handleFileUploadSuccess = (fileItem, response) => {
        // Assuming addFilesToView is a function defined elsewhere
        addFilesToView(this.props, this.state.destination, response);
    };

    closeModal = () => {
        const { showModal } = this.state;
        if (!showModal) return;

        this.setState({ showModal: false });
    };

    render() {
        const { showModal, uploader } = this.state;

        return (
            <>
                <button onClick={() => this.setState({ showModal: true })}>Upload Files</button>
                {showModal && (
                    <Modal show={true} backdrop="static" keyboard={false}>
                        <div className="modal-header">
                            <h5>File Uploader</h5>
                            {/* Close button */}
                        </div>
                        <div className="modal-body">
                            <input
                                type="file"
                                onChange={(event) => {
                                    const files = event.target.files;
                                    if (files && uploader) {
                                        Array.from(files).forEach(file => {
                                            uploader.pushFileToQueue(file);
                                        });
                                    }
                                }}
                            />
                        </div>
                        {uploader &&
                            <div className="modal-footer">
                                {/* Add buttons for actions */}
                            </div>
                        }
                    </Modal>
                )}
            </>
        );
    }

    async componentDidMount() {
        const uploadUrl = await api.get('/some-endpoint-to-get-upload-url'); // Replace with actual endpoint
        if (uploadUrl) {
            this.setState({
                uploader: new FileUploader({ url: uploadUrl }),
                destination: 'your-destination' // Replace with actual destination logic
            });

            const { uploader } = this.state;
            if (uploader) {
                uploader.onSuccessItem = this.handleFileUploadSuccess;
            }
        }
    }

    componentWillUnmount() {
        this.closeModal();
    }
}

export default PrintShopUploader;

// Utility function to add files to view, replace with actual implementation
function addFilesToView(scope: any, destination: string, response: any) {
    // Add your logic here
}