import React, {useEffect, useState} from 'react';
import {ToolsContent} from "./content/ToolsContent";
import ToolsNavigationContainer from "./navigation/ToolsNavigationContainer";
import {useSelector} from "react-redux";

const ToolsBox = ({editor, type, info}) => {
    const activeIndex = useSelector(state => state.toolReducer.activeToolIndex);
    const [clickedOnce, setClickedOnce] = useState(false);

    useEffect(() => {
        const toolBoxWidth = $('#toolsBox').width();
        const menuDuration = 500;

        if (activeIndex === -1) {
            $('#toolsBox').removeClass('open').animate({'left': -toolBoxWidth + "px"}, {
                duration: menuDuration, step: function (currentLeft) {

                    if (editor.stage.centerCameraXuser) {
                        editor.stage.centerCameraXuser();
                    }
                    $('#viewsListUser').css({left: toolBoxWidth + currentLeft});
                    $('#pagesListUser').css({left: toolBoxWidth + currentLeft});

                    let pagesListUser
                    if ((pagesListUser = document.body.querySelector('#pagesListUser')) != null) {
                        pagesListUser.style.width = (window.innerWidth - (toolBoxWidth + currentLeft)) + 'px';
                    }

                    let viewsListContent
                    if ((viewsListContent = document.body.querySelector('.viewsListContent')) != null) {
                        viewsListContent.style.width = $(document.getElementById('viewsListUser')).outerWidth(true) - $(document.body.querySelector('.addPageButton')).outerWidth(true) - 100 + "px";
                    }
                }
            });

            setClickedOnce(true);
        } else if (clickedOnce) {
            $("#toolsBox").addClass('open').animate({'left': 0}, {
                duration: menuDuration, step: function (currentLeft) {

                    if (editor.stage.centerCameraXuser) {
                        editor.stage.centerCameraXuser();
                    }

                    $('#viewsListUser').css({left: toolBoxWidth + currentLeft});
                    $('#pagesListUser').css({
                        left: toolBoxWidth + currentLeft, width: window.innerWidth - (toolBoxWidth + currentLeft)
                    });
                    $('.viewsListContent').css({width: toolBoxWidth + currentLeft});

                    document.body.querySelector('.viewsListContent').style.width = (document.getElementById('viewsListUser').offsetWidth - document.getElementById('addPageButton').offsetWidth - 100) + "px";
                }
            });
        }

    }, [activeIndex]);

    return (
        <div id="toolsBox" className={`${type} displayController`}>
            <ToolsContent editor={editor} type={type} />
            <ToolsNavigationContainer />
        </div>
    );
}

export default ToolsBox