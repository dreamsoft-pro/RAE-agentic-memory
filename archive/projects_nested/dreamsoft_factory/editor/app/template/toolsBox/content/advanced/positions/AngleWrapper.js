import React, {useState} from 'react';
import { AngleButton } from './buttons/AngleButton';
import Stepper from '../../../../../components/Stepper';

const AngleWrapper = () => {

    return (
        <div className="angle-wrapper">
            <Stepper 
            />
            <AngleButton/>
        </div>
    );
};

export default AngleWrapper;
