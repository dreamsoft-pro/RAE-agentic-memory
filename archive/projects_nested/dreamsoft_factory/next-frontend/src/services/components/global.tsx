import React, { useState } from 'react';
import axios from '@/lib/api';

interface IProps {
    source: Record<string, any>;
    properties: string[];
    target?: Record<string, any>;
}

const CopyPropertiesComponent: React.FC<IProps> = ({ source, properties, target }) => {
    const [resultTarget, setResultTarget] = useState<Record<string, any>>(target || {});

    const copyProperties = () => {
        if (!target) {
            setResultTarget({});
        }
        properties.forEach((name) => {
            resultTarget[name] = source[name];
        });
    };

    return (
        <div className="flex justify-end items-center">
            <button
                onClick={copyProperties}
                className="px-4 py-2 bg-white border text-gray-700 rounded hover:bg-gray-100 focus:outline-none"
            >
                Copy Properties
            </button>
        </div>
    );
};

export default CopyPropertiesComponent;