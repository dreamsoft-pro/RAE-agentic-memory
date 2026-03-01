import React from 'react';

const Stepper = ({ onDecrease, onIncrease, onChange, label, ...props }) => {
    
    const handleInputChange = (e) => {
        const newValue = parseFloat(e.target.value) || props.min;

        if (props.min) {
            if (newValue >= props.min) {
                onChange(newValue);
            }
        } else {
            onChange(newValue);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'ArrowUp') {
            onIncrease();
        } else if (e.key === 'ArrowDown') {
            onDecrease();
        }
    };

    return (
        <div className={'adjuster-container'}>
            {label && <div className={'adjuster-description'}>{label}</div>}
            <div className={'adjuster-controls'}>
                <div 
                    className={'decrease-button'}
                    onClick={onDecrease}
                ></div>
                <input
                    className={'current-value'}
                    type={"number"}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    {...props}
                />
                <div 
                    className={'increase-button'}
                    onClick={onIncrease}
                ></div>
            </div>
        </div>
    );
};

export default Stepper;