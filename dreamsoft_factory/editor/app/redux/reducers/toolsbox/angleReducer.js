import { INCREMENT_ANGLE, DECREMENT_ANGLE } from '../../actions/changeAngle';

const initialState = {
    angle: 0
};

const angleReducer = (state = initialState, action) => {
    switch (action.type) {
        case INCREMENT_ANGLE:
            return {
                ...state,
                angle: Math.min(state.angle + 1, 360) 
            };
        case DECREMENT_ANGLE:
            return {
                ...state,
                angle: Math.max(state.angle - 1, -360) 
            };
        default:
            return state;
    }
};

export default angleReducer;
