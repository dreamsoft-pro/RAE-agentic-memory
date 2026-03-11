import api from '@/lib/api';
import { useState, useEffect } from 'react';

const UploaderThumbsModal = ({ currentDescID }: { currentDescID: string }) => {
    const [descFiles, setDescFiles] = useState(null);
    const [thumbFiles, setThumbFiles] = useState([]);

    useEffect(() => {
        const fetchDescriptionFile = async () => {
            try {
                const response = await api.get(`/getDescriptionFile/${currentDescID}`);
                setDescFiles(response.data);
            } catch (error) {
                console.error('Failed to get description file:', error);
            }
        };

        const fetchThumbFiles = async () => {
            try {
                const response = await api.get('/getFiles');
                setThumbFiles(response.data);
            } catch (error) {
                console.error('Failed to get thumbnail files:', error);
            }
        };

        // Fetch data on component mount
        fetchDescriptionFile();
        fetchThumbFiles();
    }, [currentDescID]);

    return (
        <>
            {/* Render your modal content here */}
            <div>
                {descFiles && <p>Current Description Files: {JSON.stringify(descFiles)}</p>}
                <ul>
                    {thumbFiles.map((file, index) => (
                        <li key={index}>{file}</li>
                    ))}
                </ul>
            </div>
        </>
    );
};

export default UploaderThumbsModal;