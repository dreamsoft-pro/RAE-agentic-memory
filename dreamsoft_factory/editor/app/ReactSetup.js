import {applyMiddleware, createStore} from 'redux'
import logger from 'redux-logger'
import thunk from "redux-thunk";
import rootReducer from './redux/reducers/index'

export let store;
export const reactInit = () => {
    if (window.location.pathname.includes("index")) {
        store = createStore(rootReducer, applyMiddleware( thunk));
    } else {
        store = createStore(rootReducer, applyMiddleware(logger, thunk));
    }
}
