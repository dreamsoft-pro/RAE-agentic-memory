import React from 'react'
import {Demo} from './Demo';
import {store,reactInit} from "../app/ReactSetup";
import {Provider} from "react-redux";
// import {createRoot} from "react-dom/client";

reactInit();
const root=createRoot(document.getElementById('root'))
root.render(<Provider store={store}><Demo/></Provider>)
