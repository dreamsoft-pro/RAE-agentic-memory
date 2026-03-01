import api from '@/lib/api';
import { useEffect } from 'react';

type Props = {
    modalInstance: any; // Define type according to your specific setup.
    loadMargins: () => void;
};

const MarginManagerComponent = (props: Props) => {
    const removeMargin = async (marginID: string): Promise<void> => {
        try {
            await api.delete(`margins/${marginID}`); // Assuming API follows RESTful conventions
            props.loadMargins();
            Notification.success('success');
        } catch (error) {
            Notification.error('error');
        }
    };

    useEffect(() => {
        const handleCancel = () => {
            if (props.modalInstance.close) {
                props.modalInstance.close(); 
            }
        };

        // Assuming you're handling modal events in React context, add event listener or bind this function appropriately.
        
        return () => {
            // Cleanup if needed
        };
    }, [props.modalInstance]);

    // If you need to expose removeMargin as a method for other components to call,
    // consider making it part of the component's methods or props.

    const handleRemove = (marginID: string) => {
        removeMargin(marginID);
    };

    return (
        <div>
            {/* Your component JSX */}
            <button onClick={() => handleRemove('some-margin-id')}>Remove Margin</button> {/* Example usage */}
        </div>
    );
};

export default MarginManagerComponent;

// Notification is assumed to be a custom service or hook for simplicity. Define as needed.