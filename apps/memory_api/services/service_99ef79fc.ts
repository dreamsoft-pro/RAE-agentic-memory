import axios from 'axios';
import { useState, useRef } from 'react';
import { Modal } from '@mui/material';

interface Props {
    product: any;
    file: any;
    comment: string | undefined;
    getNextPage: (page: number) => void;
}

const RejectReportModal = ({ product, file, comment, getNextPage }: Props) => {
    const [open, setOpen] = useState(false);
    const modalRef = useRef<any>(null);

    const handleSend = () => {
        ProductFileService.rejectReport(product.productID, file.ID, comment).then(response => {
            if (response.data.response) { // Assuming response is an object with a `data` property
                console.log('Report rejected', file.name);
                modalRef.current.close();
                getNextPage(1); // Assuming you want to go back to the first page after closing modal
            }
        });
    };

    return (
        <Modal open={open} onClose={() => setOpen(false)}>
            <div>
                <button onClick={() => setOpen(true)}>Reject Report</button>
                {open && (
                    <div ref={modalRef}>
                        {/* Add your form elements here */}
                        <input type="text" placeholder="Enter comment" onChange={(e) => setComment(e.target.value)} />
                        <button onClick={handleSend}>Send</button>
                    </div>
                )}
            </div>
        </Modal>
    );
};

const ProductFileService = {
    rejectReport: (productID: string, fileID: string, comment: string) =>
        axios.post(`/api/reject-report/${productID}/${fileID}`, { comment }),
};

export default RejectReportModal;