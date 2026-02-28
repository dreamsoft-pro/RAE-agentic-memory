import React, {useEffect} from "react";

/**
 * Generuje przycisk do auto uzupełniania
 */
const FillImagesAutomaticallyButton = ({editor, usedInModal = false, ...props}) => {

    const handleClick = (e) => {
        e.stopPropagation();

        editor.webSocketControllers.userProject.autoFill(editor.userProject.getID(), function (data) {

            editor.userProject.regenerateViewThumb();
            editor.userProject.redrawView();
            //_this.editor.webSocketControllers.userProject.getProjectImagesUseNumber( _this.editor.userProject.getID() );
            /*
            _this.editor.webSocketControllers.userView.get( _this.editor.userProject.getCurrentView()._id, function( view_ ){

                console.log( _this.editor.userProject.getCurrentView() );
                console.log( view_ );
                console.log('CO TO ZA WIDOK DO ZALADOWANIA???');
                console.log('_____________+++++++++++++++++++++_____________');
                _this.editor.userProject.initView( view_ );

            });
            */
        });
    }

    return (
        <button
            // stara klasa
            // className={'button-fn autofill'}
            {...props}
            className={`main-tool-button gray ${usedInModal && "disable-actions"}`}
            onClick={(e) => handleClick(e)}
        >
            Auto Uzupełnianie
        </button>
    )
}

export default FillImagesAutomaticallyButton