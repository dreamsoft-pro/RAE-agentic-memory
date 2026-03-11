import api from '@/lib/api';
import { useEffect, useState } from 'react';

const MyComponent = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/some-endpoint');
                setData(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            {/* Render your component UI using the `data` state */}
            {JSON.stringify(data)}
        </div>
    );
};

export default MyComponent;