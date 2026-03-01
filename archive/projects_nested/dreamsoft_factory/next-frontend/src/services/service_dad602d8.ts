import React, { useEffect, useState } from 'react';
import api from '@/lib/api'; // Assuming this is a custom axios instance

interface SpinnerSliderProps {
    model: number;
    min?: string;
    max?: string;
    step?: string;
    onChange?(value: number): void; // Optional callback to notify when the value changes
}

const SpinnerSlider: React.FC<SpinnerSliderProps> = ({ model, min, max, step, onChange }) => {
    const [currentValue, setCurrentValue] = useState<number>(model);

    useEffect(() => {
        if (min) {
            setCurrentValue(Math.max(Number(min), currentValue));
        }
        if (max && currentValue > Number(max)) {
            setCurrentValue(Number(max));
        }
    }, [min, max]);

    const decrement = () => {
        let newValue = Math.max(Number(min || 0), currentValue - (step ? Number(step) : 1));
        setCurrentValue(newValue);
        onChange?.(newValue); // Call back with new value if provided
    };

    const increment = () => {
        let newValue = Math.min(currentValue + (step ? Number(step) : 1), Number(max || Infinity));
        setCurrentValue(newValue);
        onChange?.(newValue); // Call back with new value if provided
    };

    return (
        <div className="input-group spincontainer">
            <button type="button" className="btn btn-default" onClick={decrement} data-dir="dwn"><i className="fa fa-minus"></i></button>
            <input 
                className="form-control spinner-input"
                type="number"
                value={currentValue}
                onChange={(e) => setCurrentValue(Number(e.target.value))}
                min={min || '0'}
                max={max}
                step={step ? Number(step) : undefined} />
            <button type="button" className="btn btn-default" onClick={increment} data-dir="up"><i className="fa fa-plus"></i></button>
        </div>
    );
};

export default SpinnerSlider;