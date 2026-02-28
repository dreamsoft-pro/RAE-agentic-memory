import { TOGGLE_VIEWS, TOGGLE_PAGES } from '../../actions/carousel';

const initialState = {
    isViewsOpen: true,
    isPagesOpen: true,
};
  
export const carouselReducer = (state = initialState, action) => {
    switch (action.type) {
        case TOGGLE_VIEWS:
            return { ...state, isViewsOpen: !state.isViewsOpen };
        case TOGGLE_PAGES:
            return { ...state, isPagesOpen: !state.isPagesOpen };
        default:
            return state;
    }
};