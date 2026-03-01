import React, {useState} from 'react';
import { AngleButton } from './buttons/AngleButton';
import Stepper from '../../../../components/Stepper';
import { useSelector } from 'react-redux';


const AngleWrapper = () => {

    const { proposedPositionInstance } = useSelector(state => state.selectedImageReducer);

    const [angle, setAngle] = useState(parseInt(proposedPositionInstance.rotation))

    const onDecrease = () => {
        const newAngle = angle - 1 < -360 ? 360 : angle - 1;
        setAngle(newAngle);
        changeAngle(newAngle, true);
    };
    
    const onIncrease = () => {
        const newAngle = angle + 1 > 360 ? -360 : angle + 1;
        setAngle(newAngle);
        changeAngle(newAngle, true);
    };

    const changeAngle = (newAngle, save) => {
        newAngle = parseInt(newAngle);
        proposedPositionInstance.editor.getEditableObjectsByType('singleElem', 'ProposedPosition')
            .forEach(editingObject => {
                editingObject.setRotation(newAngle);
                if (save) {
                    proposedPositionInstance.editor.webSocketControllers.proposedImage.setAttributes(
                        editingObject.dbID,
                        {
                            rotation: newAngle
                        }
                    );
                }
            });
    };
   
    return (
        <div className="angle-wrapper">
            <Stepper 
                onDecrease={onDecrease} 
                onIncrease={onIncrease} 
                onChange={(newAngle) => { 
                    setAngle(newAngle); 
                    changeAngle(newAngle, true);
                }} 
                value={angle}
                min={-360}
                max={360}
            />
            <AngleButton/>
        </div>
    );
};

export default AngleWrapper;
