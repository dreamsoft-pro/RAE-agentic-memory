import React from 'react'
import TextTools from "../app/class/tools/textTools";

window.userType = 'admin'
export default function () {
    const conf = {
        getGlobalPosition: () => {
            return [0,0]
        },
        getTransformedBounds: () => {
            return {width:100, height:100}
        },
        editor: {
            getStage: () => {
                return {scaleX:1, scaleY:1}
            },
            userType: 'admin', fonts: {
                selectFont: () => {
                }, getFonts: () => {
                    return {}
                }, getFontFeatures: () => {
                    return {
                        italic: false,
                        bold: false
                    }
                },
                addFontFile:()=>{}
            }
        }
    }
    return <TextTools textInstance={conf}/>
}
