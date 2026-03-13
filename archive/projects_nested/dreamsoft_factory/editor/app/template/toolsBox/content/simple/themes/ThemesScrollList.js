import React from 'react'
import {useSelector} from "react-redux";

const ThemesScrollList  = ({editor}) => {
    const {themes} = useSelector(state => state.projectReducer)

    const handleClick = (theme) => {

        // this needs to be implemented properly
        // editor.webSocketControllers.userProject.setMainTheme(editor.userProject.getID(), theme._id, (editor) => editor.userProject.initTheme(theme._id))
    }
    // var elem = document.createElement('div');
    // elem.className = 'userThemePage' + ((data.vacancy) ? ' vacancy' : ' noVacancy');
    // elem.style.backgroundImage = 'url(' + EDITOR_ENV.staticUrl + data.url + ')';
    // elem.setAttribute('theme-page-id', data._id);
    //
    // var elemName = document.createElement('div');
    // elemName.className = 'title';
    // elemName.innerHTML = data.name;
    return (
        <div className="themes-scroll-list">
            <div className="grid-container three-columns">
                {Object.entries(themes).map(([_, theme], index) => (
                    <div
                        onClick={() => handleClick(theme)}
                        className={'single-theme'}
                        key={index}>
                        <img
                            src={
                                `${EDITOR_ENV.staticUrl + theme.url}`
                            }
                            className={'theme-photo'}
                        />
                        <div className={'theme-caption'}>
                            {theme.name}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

// {[...Array(9)].map((_, i) => (
//     <div key={i} className="grid-item">
//         {/*<img*/}
//         {/*    src="../../../../images/ThemesWomanFoto.png"*/}
//         {/*    alt={`Motyw ${i + 1}`}*/}
//         {/*    className="grid-foto"*/}
//         {/*/>*/}
//         <div className="grid-caption">
//             Motyw {i + 1}
//         </div>
//     </div>
// ))}

export default ThemesScrollList
