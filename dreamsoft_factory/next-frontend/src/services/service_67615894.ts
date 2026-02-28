import axios from 'axios';
import React, { Component } from 'next';

class RejectModal extends Component {
    state = {
        comment: ''
    };

    send = () => {
        const { comment } = this.state;
        // Perform your API call using axios here
        axios.post('/your-endpoint', { comment })
            .then(response => {
                console.log('Success:', response);
                // Handle success
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle error
            });
    };

    render() {
        return (
            <div className="modal">
                <div className="modal-header">
                    <h4 className="modal-title">Give reason of rejection</h4>
                </div>
                <div className="modal-body">
                    <textarea 
                        value={this.state.comment} 
                        onChange={(e) => this.setState({ comment: e.target.value })}
                        className="form-control" 
                        placeholder="Comment"
                    />
                </div>
                <div className="modal-footer">
                    <button className="btn btn-default" onClick={() => this.props.onClose()}>Cancel</button>
                    <button className="btn btn-success" onClick={this.send}><i className="fa fa-check"></i> Submit</button>
                </div>
            </div>
        );
    }
}

export default RejectModal;