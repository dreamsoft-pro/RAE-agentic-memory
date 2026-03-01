import UserPagePreview from "./../UserPagePreview";
import TopMenu from "../topMenu/TopMenu";
import React from "react";
import {createRoot} from "react-dom/client";
import {store} from '../../ReactSetup';
import {Provider, useSelector} from 'react-redux';
import ImagesToolContent from "../toolsBox/content/simple/images/ImagesToolContent";
import ToolsBox from "../toolsBox/ToolsBox";
import {ProjectImage} from "../../class/ProjectImage";
import {updateTemplatesData} from "../../redux/reducers/templates/templates";
import HeaderInfoModal from "../modals/HeaderInfoModal";
import HeaderVideosModal from "../modals/HeaderVideosModal";
import RemoveAllImagesModal from "../modals/RemoveAllImagesModal";
import RemoveSinglePhotoModal from "../modals/RemoveSinglePhotoModal";
import CarouselBox from "../carousel/CarouselBox";
import ProposedPositionContextMenu from "../../class/tools/ProposedPositionContextMenu2_user";
import CanvasTools from "../../components/canvasTools/CanvasTools";

var TemplateModule = require('./main').TemplateModule;

var bottomBoxOpen = true;
var stageBottomThemesBox = false;

var menuDuration = 500;
var helperDuration = 300;

TemplateModule.prototype.stageBottomBox = function (value) {

    if (value) {
        bottomBoxOpen = value;
    }
    return bottomBoxOpen;
}

TemplateModule.prototype.stageBottomThemesBox = function (value) {

    if (value) {
        stageBottomThemesBox = value;
    }
    return stageBottomThemesBox;
}

TemplateModule.prototype.generatePages = function () {

    var tool = document.createElement('div');
    tool.id = 'pages-container-tool';
    tool.className = 'tool closed';
    //tool.style.width = '1200px';

    var innerContainer = document.createElement('div');
    innerContainer.className = 'innerContainer';

    var toolButton = document.createElement('span');
    toolButton.id = 'pages-container-tool_button';
    toolButton.className = 'tool-button';
    toolButton.setAttribute('data-content', 'pages-content');

    tool.appendChild(toolButton);

    var toolHelper = document.createElement('span');
    toolHelper.className = 'toolHelper';
    toolHelper.innerHTML = '<i></i><span>Podgląd stron</span>';

    tool.appendChild(toolHelper);
    // views content
    var toolContent = document.createElement('div');
    toolContent.id = 'pages-content';


    var viewsList = document.createElement('ul');
    viewsList.id = 'pages-list';

    toolContent.appendChild(viewsList);

    var toolsContainer = document.getElementById("toolsContent");
    toolsContainer.appendChild(toolContent);


    // programowanie przycisku views
    toolButton.addEventListener('click', function () {


    });

    //funkcje inicjalizujące
    return tool;

};

TemplateModule.prototype.updateUserThemes = function (themes) {

    var Editor = this.editor;

    var themeContent = document.getElementById('project-themes-list');

    for (var i = 0; i < themes.length; i++) {

        var themeTitle = document.createElement('span');
        themeTitle.className = 'themeName';
        themeTitle.innerHTML = themes[i].name;
        themeTitle.setAttribute('data-theme-name', themes[i].name);

        var showPages = document.createElement('span');
        showPages.className = 'EditPages';
        showPages.addEventListener('click', function () {

            //Editor.template.overlayBlock( content, 'big');

        });


        var theme = document.createElement('li');
        theme.setAttribute('data-theme-id', themes[i]._id);
        theme.setAttribute('data-main-theme-id', themes[i].MainTheme);
        theme.appendChild(themeTitle);
        theme.style.backgroundImage = 'url(' + themes[i].url + ')';

        theme.addEventListener('click', function (e) {

            e.stopPropagation();

            stageBottomThemesBox = true;


            if ($('#pagesListUser').attr('isopen') == 'true' || $('#pagesListUser').attr('isopen') == undefined) {

                if ($('#viewsListUser').attr('isopen') == 'true' || $('#viewsListUser').attr('isopen') == undefined) {
                    $('#viewsListUser').attr('isopen', 'false');

                    $('#viewsListUser').animate({bottom: -110}, function () {


                    });

                }


            } else {

                $('#pagesListUser').attr('isopen', 'true');
                $("#pagesListUser").animate({bottom: 0}, {

                    duration: 200,
                    step: function (topStep) {
                        Editor.template.resizeToUserObject();
                        Editor.stage.centerCameraYuser();

                    },
                    complete: function () {

                        Editor.template.resizeToUserObject();
                        Editor.stage.centerCameraYuser();

                    }

                });

                if ($('#viewsListUser').attr('isopen') == 'true' || $('#viewsListUser').attr('isopen') == undefined) {
                    $('#viewsListUser').attr('isopen', 'false');

                    $('#viewsListUser').animate({bottom: -110}, function () {


                    });

                }

            }

            Editor.webSocketControllers.theme.get(this.getAttribute('data-theme-id'), function (data) {
                var pagesListUser = document.getElementById('pagesListUser').querySelector('.pagesListContent');
                pagesListUser.innerHTML = '';

                for (var i = 0; i < data.ThemePages.length; i++) {
                    var themePage = data.ThemePages[i];
                    pagesListUser.appendChild(Editor.template.elements.userThemePage(themePage));

                }


            });
            //alert('teraz ma sie wyswietlic lista stron motywu');

        });

        themeContent.appendChild(theme);

    }

};

TemplateModule.prototype.generateViewsPagesThumb = function () {

    var tempLenght = [];
    tempLenght = Editor.userProject.getViewsNumber();
    var numberOfViews = tempLenght.length;

    for (var i = 0; i <= numberOfViews - 1; i++) {

        var promise = Editor.userProject.turnToNextView().done(function () {

        });

    }

    // var loadPageView =  Editor.userProject.getViewsNumber()[0];
    //Editor.userProject.initView( loadPageView );

}

TemplateModule.prototype.viewSnapShot = function () {

    var promise = Editor.userProject.turnToNextView().done(function () {

    });


}


TemplateModule.prototype.setMainThemeForUserProject = function (themes) {

    var body = document.createElement('div');
    body.className = 'all-theme-list';
    var _this = this;

    for (var i = 0; i < themes.length; i++) {

        var themeTitle = document.createElement('span');
        themeTitle.className = 'themeName';
        themeTitle.innerHTML = themes[i].name;
        themeTitle.setAttribute('data-theme-name', themes[i].name);

        var showPages = document.createElement('span');
        showPages.className = 'EditPages';
        showPages.addEventListener('click', function () {

            //Editor.template.overlayBlock( content, 'big');

        });


        var theme = document.createElement('li');
        theme.setAttribute('data-theme-id', themes[i]._id);
        theme.setAttribute('data-main-theme-id', themes[i].MainTheme);
        theme.appendChild(themeTitle);
        theme.style.backgroundImage = 'url(' + themes[i].url + ')';

        theme.addEventListener('click', function (e) {

            e.stopPropagation();

            // stageBottomThemesBox = true ;

            var mainThemeID = this.getAttribute('data-theme-id');

            _this.editor.webSocketControllers.userProject.setMainTheme(_this.editor.userProject.getID(), mainThemeID, function (data) {

                _this.editor.webSocketControllers.theme.get(mainThemeID, function (data) {

                    _this.updateCliparts(data.MainTheme.ProjectCliparts);

                    _this.editor.userProject.setMasks(data.MainTheme.ProjectMasks);

                    var pagesListUser = document.getElementById('pagesListUser').querySelector('.pagesListContent');
                    pagesListUser.innerHTML = '';

                    for (var i = 0; i < data.ThemePages.length; i++) {
                        var themePage = data.ThemePages[i];
                        pagesListUser.appendChild(_this.editor.template.elements.userThemePage(themePage));

                    }

                    _this.editor.dialogs.modalHide('#setMainTheme-window');

                });

                _this.editor.webSocketControllers.userView.get(_this.editor.userProject.getCurrentView()._id, function (data) {

                    _this.editor.userProject.initView(data);

                    setTimeout(function () {

                        _this.editor.userProject.regenerateViewThumb();

                    }, 1000);

                });


            });


        });

        body.appendChild(theme);

    }

    var smallWindow = this.editor.template.displayWindow(
        'setMainTheme-window',
        {

            size: 'small',
            title: 'Wybierz motyw przewodni',
            content: body

        },
        true
    );

    $('body').append(smallWindow);


    $('#setMainTheme-window').on('hidden.bs.modal', function () {

        $(this).remove();

    });

    const modal = this.editor.dialogs.modalCreate('#setMainTheme-window', {

        keyboard: false,
        backdrop: 'static'

    });
    modal.show()

};

TemplateModule.prototype.updateUserViews = function (views) {

    var currentPage = 0;

    var _this = this;

    _this.userPagesPreview.removeAllViews();


    function createViewElement(view) {

        if (view.views) {

            var pagesValue = 0;

            for (var i = 0; i < view.Pages.length; i++) {

                pagesValue += view.Pages[i].pageValue;

            }

            _this.userPagesPreview.addComplexView(pagesValue, view.repeatable, view._id, view.order);
            currentPage += pagesValue;

        } else {

            var pagesValue = 0;

            for (var i = 0; i < view.Pages.length; i++) {

                pagesValue += view.Pages[i].pageValue;

            }

            _this.userPagesPreview.addView(pagesValue, view.repeatable, view._id, view.order);
            currentPage += pagesValue;

        }

    };

    for (var i = 0; i < views.length; i++) {

        createViewElement(views[i]);

    }

};

TemplateModule.prototype.updateUserComplexViews = function (projects) {

    var currentPage = 0;

    var _this = this;

    _this.userPagesPreview.removeAllViews();

    function createViewElement(project) {

        let productName = '';

        for (var key in _this.editor.productsNames) {

            if (_this.editor.productsNames[key].indexOf(project.typeID) > -1) {
                productName = key;
                break;
            }

        }

        _this.userPagesPreview.addComplexView(project.typeID, project.Views, productName, project._id);

    };

    for (var i = 0; i < projects.length; i++) {

        createViewElement(projects[i]);

    }

};

TemplateModule.prototype.displayUserPhotos = function (userID) {


    Editor.webSocketControllers.user.getPhotos(userID, function (data) {

        var photos = document.createElement('div');
        photos.id = 'currentUserPhotos';

    });

};


TemplateModule.prototype.generateSwapTemplate = function () {

    var elem = document.createElement('div');
    elem.id = 'swapLayout';

    elem.addEventListener('click', function (e) {

        e.stopPropagation();

    });

    return elem;

};


TemplateModule.prototype.nextPageAndPreviousPage = function () {

    var elem = document.createElement('div');
    elem.id = 'pageController';

    var next = document.createElement('div');
    next.className = 'nextPageButton';

    next.addEventListener('click', function (e) {

        e.stopPropagation();

    });

    var prevButtonAndLabel = document.createElement('div')
    prevButtonAndLabel.className = 'prevButtonAndLabel';

    var nextButtonAndLabel = document.createElement('div')
    nextButtonAndLabel.className = 'nextButtonAndLabel';

    var prev = document.createElement('div');
    prev.className = 'prevPageButton';

    var prevLabel = document.createElement('label');
    prevLabel.className = 'prevLabel';

    var nextLabel = document.createElement('label');
    nextLabel.className = 'nextLabel';


    prev.appendChild(prevLabel);
    next.appendChild(nextLabel);

    prev.addEventListener('click', function (e) {

        e.stopPropagation();

    });

    prevButtonAndLabel.appendChild(prev);
    nextButtonAndLabel.appendChild(next);

    elem.appendChild(prevButtonAndLabel);
    elem.appendChild(nextButtonAndLabel);

    return elem;

};

TemplateModule.prototype.changeViewThumb = function (viewID, thumb) {

    this.userPagesPreview.changeViewThumb(viewID, thumb);

};

TemplateModule.prototype.generateLayersTool = function () {

    // var tool = document.createElement('div');
    // tool.id = 'layers-container-tool';
    // tool.className = 'tool closed';
    //
    // var innerContainer = document.createElement('div');
    // innerContainer.id = 'layersContent';
    //
    //
    // var layers = document.createElement('div');
    // layers.id = 'editorLayers';
    //
    // var toolMainContent = document.createElement('div');
    // toolMainContent.id = "layers-main-content"
    //
    // innerContainer.appendChild(toolMainContent);
    // toolMainContent.appendChild(layers);
    //
    // var toolsContainer = document.getElementById("toolsContent");
    // toolsContainer.appendChild(innerContainer);
    //
    // return tool;
};

TemplateModule.prototype.generateUserViewsAndThemes = function () {

    var tool = document.createElement('div');
    tool.id = 'layers-container-tool';
    tool.className = 'tool closed';

    var innerContainer = document.createElement('div');
    innerContainer.id = 'layersContent';


    var layers = document.createElement('div');
    layers.id = 'editorLayers';

    var toolMainContent = document.createElement('div');
    toolMainContent.id = "layers-main-content"

    innerContainer.appendChild(toolMainContent);
    toolMainContent.appendChild(layers);

    var toolsContainer = document.getElementById("toolsContent");
    toolsContainer.appendChild(innerContainer);

    return tool;
};

TemplateModule.prototype.generateUserViewsAndThemes = function () {

    // var Editor = this.editor;

    // var carouselBox = document.createElement('div');
    // carouselBox.id = 'carouselBox';
    // carouselBox.classList.add('carouselBox');
    // //TODO document.getElementById(...) is null
    // var viewsList = document.createElement('ul');
    // viewsList.id = 'ulviewsList';
    // var viewCount = 1;

    // var viewsListUser = document.createElement('div');
    // viewsListUser.id = 'viewsListUser';
    // viewsListUser.className = 'displayController';
    // viewsListUser.setAttribute('isopen', 'true');
    // carouselBox.appendChild(viewsListUser);
    // document.body.appendChild(carouselBox);

    // var viewsListContent = document.createElement('div');
    // viewsListContent.className = 'viewsListContent';

    // var viewsListLabel = document.createElement('div');
    // viewsListLabel.className = 'viewsListLabel';

    // viewsListLabel.addEventListener('click', () => {
    //     viewsListLabel.classList.toggle('active');
    // })

    // var viewsListHorRuler = document.createElement('div');
    // viewsListHorRuler.className = 'viewsListHorRuler';

    // var mainButtonsTool = document.createElement('div');
    // mainButtonsTool.id = 'mainViewsButtons';

    // var addPageButton = document.createElement('div');
    // addPageButton.id = 'addPageButton';
    // addPageButton.className = 'actionButton';
    // mainButtonsTool.appendChild(addPageButton);

    // var addPageButtonDesc = document.createElement('span');
    // addPageButtonDesc.id = 'addPageButtonDesc';
    // addPageButtonDesc.className = 'actionButtonDesc';
    // addPageButtonDesc.innerHTML = 'Add Page';
    // addPageButton.appendChild(addPageButtonDesc);

    // var allPagesPopUpButton = document.createElement('div');
    // allPagesPopUpButton.id = 'allPagesPopUpButton';
    // allPagesPopUpButton.className = 'actionButton';
    // mainButtonsTool.appendChild(allPagesPopUpButton);

    // var allPagesPopUpButtonDesc = document.createElement('span');
    // allPagesPopUpButtonDesc.id = 'allPagesPopUpButtonDesc';
    // allPagesPopUpButtonDesc.className = 'actionButtonDesc';
    // allPagesPopUpButtonDesc.innerHTML = 'Sort';
    // allPagesPopUpButton.appendChild(allPagesPopUpButtonDesc);

    // var scrollViewsLeft = document.createElement('div');
    // scrollViewsLeft.id = 'scrollViewsLeft';
    // scrollViewsLeft.className = 'scrollButton';

    // var scrollViewsRight = document.createElement('div');
    // scrollViewsRight.id = 'scrollViewsRight';
    // scrollViewsRight.className = 'scrollButton';

    // var scrollThemesLeft = document.createElement('div');
    // scrollThemesLeft.id = 'scrollThemesLeft';
    // scrollThemesLeft.className = 'scrollButton';

    // var scrollThemesRight = document.createElement('div');
    // scrollThemesRight.id = 'scrollThemesRight';
    // scrollThemesRight.className = 'scrollButton';

    // viewsListUser.appendChild(mainButtonsTool);

    // viewsListUser.appendChild(scrollViewsLeft);

    // addPageButton.addEventListener('click', function (e) {

    //     e.stopPropagation();
    //     const proj = this.editor.userProject.getObj().projects[this.editor.userProject.getObj().projects.length - 1];//TODO Nie zawsze ostatni
    //     if (this.editor.checkPagesCountConstraint({project: proj, addRemove: 'ADD'})) {
    //         let pos = this.editor.userProject.getCurrentView().order + 1;
    //         if (pos === proj.Views.length) {
    //             pos--;
    //         }
    //         this.editor.webSocketControllers.userProject.addNewView(proj._id, pos);
    //     }
    // }.bind(this));

    // allPagesPopUpButton.addEventListener('click', function (e) {

    //     e.stopPropagation();

    //     this.editor.template.displayAllPagesWithPhotos();

    // }.bind(this));

    // viewsList.addEventListener('click', function (e) {

    //     e.stopPropagation();

    //     if (e.target && e.target.nodeName == "LI") {

    //         this.editor.webSocketControllers.userView.get(e.target.getAttribute('user-view-id'), function (data) {

    //             this.editor.userProject.updateCurrentViewThumb();
    //             this.editor.userProject.initView(data);

    //         }.bind(this));

    //     } else if (e.target && e.target.nodeName == "DIV" && e.target.className == 'viewRemover') {

    //         e.stopPropagation();
    //         if (this.editor.checkPagesCountConstraint({
    //             project: this.editor.userProject.getObj().projects[this.editor.userProject.getObj().projects.length - 1],
    //             addRemove: 'REMOVE'
    //         })) {//TODO Valid simple index
    //             this.editor.webSocketControllers.userProject.removeView(this.editor.userProject.getID(), e.target.getAttribute('user-view-id'));
    //         }

    //     }

    // }.bind(this));


    // //viewsListContent.appendChild( viewsList );

    // document.getElementById("viewsListUser").appendChild(viewsListLabel);
    // document.getElementById("viewsListUser").appendChild(viewsListContent);
    // viewsListUser.appendChild(scrollViewsRight);

    // var _this = this;

    // viewsListLabel.addEventListener('click', function (e) {

    //     e.stopPropagation();

    //     //var _this = this;

    //     if ($("#viewsListUser").attr('isopen') == 'true' || $("#viewsListUser").attr('isopen') == undefined) {

    //         $("#viewsListUser").attr('isopen', 'false');
    //         $("#viewsListUser").animate({bottom: -110}, {

    //             duration: 200,
    //             step: function (topStep) {

    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();

    //             },
    //             complete: function () {

    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();

    //             }

    //         });

    //     } else {

    //         if ($('#pagesListUser').attr('isopen') == 'false') {

    //             $("#pagesListUser").animate({bottom: 0}, 200, function () {


    //             });

    //         }

    //         $("#pagesListUser").attr('isopen', 'true');
    //         $("#viewsListUser").attr('isopen', 'true');

    //         $("#viewsListUser").animate({bottom: 0}, {

    //             duration: 200,
    //             step: function (topStep) {
    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();

    //             },
    //             complete: function () {

    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();

    //             }

    //         });

    //     }

    // });

    // viewsListContent.style.width = viewsListUser.offsetWidth - addPageButton.offsetWidth - 100 + 'px';
    // viewsListContent.style.height = '110px';

    // if (viewsList.childNodes[0]) {

    //     viewsList.style.width = viewsList.childNodes.length * (viewsList.childNodes[0].offsetWidth + 10) + "px";


    // } else {

    //     viewsList.style.width = '200px';

    // }

    // window.addEventListener('resize', function (e) {

    //     viewsListContent.style.width = viewsListUser.offsetWidth - addPageButton.offsetWidth - 100 + 'px';

    // });

    // Ps.initialize(viewsListContent, {

    //     useBothWheelAxes: true

    // });

    // scrollViewsLeft.addEventListener('click', function (e) {
    //     viewsListContent.scrollLeft -= 240;
    //     Ps.update(viewsListContent);
    // });

    // scrollViewsRight.addEventListener('click', function (e) {
    //     viewsListContent.scrollLeft += 240;
    //     Ps.update(viewsListContent);
    // });

    // var pagesListUser = document.createElement('div');
    // pagesListUser.id = 'pagesListUser';
    // pagesListUser.className = 'displayController';
    // pagesListUser.setAttribute('isopen', 'true');

    // const top = document.createElement('div');
    // top.id = 'topPagesListUser';
    // const bottom = document.createElement('div');
    // bottom.id = 'bottomPagesListUser';

    // pagesListUser.appendChild(top);
    // pagesListUser.appendChild(bottom);

    // //pagesListUser.className = ( ( Editor.userProject.getCurrentView().Pages[0].vacancy ) ? 'vacancy' : 'noVacancy' ) + '';

    // var pagesCont = document.createElement('div');
    // pagesCont.className = 'currentPagesSwitcher';

    // var prevPage = document.createElement('div');
    // prevPage.className = 'prevPage';

    // var nextPage = document.createElement('div');
    // nextPage.className = 'nextPage';

    // var currentPageInfo = document.createElement('div');
    // currentPageInfo.className = 'currentPageInfo';

    // var pagesControllers = document.createElement('div');
    // pagesControllers.className = 'pagesControllers';

    // var pagesInfo = document.createElement('div');
    // pagesInfo.className = 'pagesInfo';

    // pagesControllers.appendChild(prevPage);
    // pagesControllers.appendChild(currentPageInfo);
    // pagesControllers.appendChild(pagesInfo);
    // pagesControllers.appendChild(nextPage);

    // pagesCont.appendChild(pagesControllers);

    // var pageListButtons = document.createElement('div');
    // pageListButtons.id = 'pageListButtons';

    // var applyPageButton = document.createElement('div');
    // applyPageButton.id = 'applyPageButton';
    // applyPageButton.className = 'actionButton';
    // pageListButtons.appendChild(applyPageButton);

    // var applyPageButtonDesc = document.createElement('span');
    // applyPageButtonDesc.id = 'applyPageButtonDesc';
    // applyPageButtonDesc.className = 'actionButtonDesc';
    // applyPageButtonDesc.innerHTML = 'Apply to page';
    // applyPageButton.appendChild(applyPageButtonDesc);

    // var applyAllPagesButton = document.createElement('div');
    // applyAllPagesButton.id = 'applyAllPagesButton';
    // applyAllPagesButton.className = 'actionButton';
    // pageListButtons.appendChild(applyAllPagesButton);

    // var applyAllPagesButtonDesc = document.createElement('span');
    // applyAllPagesButtonDesc.id = 'applyAllPagesButtonDesc';
    // applyAllPagesButtonDesc.className = 'actionButtonDesc';
    // applyAllPagesButtonDesc.innerHTML = 'For all pages';
    // applyAllPagesButton.appendChild(applyAllPagesButtonDesc);


    // // TODO - carousel
    // // carouselBox.appendChild(pagesCont);
    // top.appendChild(pagesCont);

    // pagesListUser.style.width = (window.innerWidth - 310) + 'px';

    // var pagesListHorRuler = document.createElement('div');
    // pagesListHorRuler.className = 'pagesListHorRuler';

    // var pagesListHeader = document.createElement('div');
    // pagesListHeader.className = 'pagesListHeader';

    // pagesListHeader.addEventListener('click', () => {
    //     pagesListHeader.classList.toggle('active');
    // })

    // top.appendChild(pagesListHeader);
    // //pagesListUser.appendChild( pagesListHorRuler );
    // top.appendChild(viewsListLabel);

    // var pagesListContent = document.createElement('div');
    // pagesListContent.className = 'pagesListContent';

    // Ps.initialize(pagesListContent, {

    //     useBothWheelAxes: true

    // });

    // scrollThemesLeft.addEventListener('click', function (e) {
    //     pagesListContent.scrollLeft -= 240;
    //     Ps.update(pagesListContent);
    // });

    // scrollThemesRight.addEventListener('click', function (e) {
    //     pagesListContent.scrollLeft += 240;
    //     Ps.update(pagesListContent);
    // });

    // $('#pagesListUser').remove();
    // // document.body.appendChild(pagesListUser);

    // prevPage.addEventListener('click', function (e) {

    //     e.stopPropagation();
    //     Editor.userProject.turnToPreviousView().then(function () {

    //         var pagesListUser = document.getElementById('pagesListUser');

    //         if (pagesListUser) {

    //             if (Editor.userProject.getCurrentView().Pages[0].vacancy) {

    //                 $(pagesListUser).removeClass('noVacancy');
    //                 $(pagesListUser).addClass('vacancy');

    //             } else {

    //                 $(pagesListUser).removeClass('vacancy');
    //                 $(pagesListUser).addClass('noVacancy');

    //             }

    //         }

    //     });

    // });

    // nextPage.addEventListener('click', function (e) {

    //     e.stopPropagation();
    //     Editor.userProject.turnToNextView().then(function () {

    //         var pagesListUser = document.getElementById('pagesListUser');

    //         if (pagesListUser) {

    //             if (Editor.userProject.getCurrentView().Pages[0].vacancy) {

    //                 $(pagesListUser).removeClass('noVacancy');
    //                 $(pagesListUser).addClass('vacancy');

    //             } else {

    //                 $(pagesListUser).removeClass('vacancy');
    //                 $(pagesListUser).addClass('noVacancy');

    //             }

    //         }

    //     });

    // });

    // applyPageButton.addEventListener('click', function (e) {

    //     e.stopPropagation();       

    //     var Editor = this.editor;

    //     const selectedTheme = document.querySelector('.userThemePage.selected')

    //     if (selectedTheme) {

    //         const pages = Editor.stage.getPages();
            
    //         if(!pages.length) {
    //             console.log("tablica Editor.stage.pages jest pusta"); // TODO - do usuniecia
    //             return;
    //         }

    //         Editor.webSocketControllers.userPage.useThemePage(Editor.stage.getPages()[0].userPage._id, selectedTheme.getAttribute('theme-page-id'), function (data) {

    //             store.dispatch(updateTemplatesData(data.themePage.proposedTemplates));
    //             Editor.stage.getPages()[0].loadThemePage(data.themePage);
    //             Editor.stage.getPages()[0].loadTemplate(data.proposedTemplate, data.usedImages);

    //         });

    //         selectedTheme.classList.remove('selected');

    //     }

    // }.bind(this));

    // pagesListHeader.addEventListener('click', function (e) {

    //     e.stopPropagation();

    //     if ($('#pagesListUser').attr('isopen') == 'true' || $('#pagesListUser').attr('isopen') == undefined) {

    //         if ($('#viewsListUser').attr('isopen') == 'true' || $('#viewsListUser').attr('isopen') == undefined) {
    //             $('#viewsListUser').attr('isopen', 'false');

    //             $('#viewsListUser').animate({bottom: -110}, function () {


    //             });

    //         } else {

    //             $('#pagesListUser').attr('isopen', 'false');
    //             $("#pagesListUser").animate({bottom: -110}, {

    //                 duration: 200,
    //                 step: function (topStep) {

    //                     _this.editor.template.resizeToUserObject();
    //                     _this.editor.stage.centerCameraYuser();

    //                 },
    //                 complete: function () {

    //                     _this.editor.template.resizeToUserObject();
    //                     _this.editor.stage.centerCameraYuser();
    //                 }
    //             });

    //         }


    //     } else {

    //         $('#pagesListUser').attr('isopen', 'true');
    //         $("#pagesListUser").animate({bottom: 0}, {

    //             duration: 200,
    //             step: function (topStep) {
    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();

    //             },
    //             complete: function () {

    //                 _this.editor.template.resizeToUserObject();
    //                 _this.editor.stage.centerCameraYuser();
    //             }

    //         });

    //     }

    // });

    // bottom.appendChild(pageListButtons);
    // bottom.appendChild(scrollThemesLeft);
    // bottom.appendChild(pagesListContent);
    // bottom.appendChild(scrollThemesRight);
    // carouselBox.appendChild(pagesListUser);
    // ReactDOM.render(<Provider store={store}><UserPagePreview editor={this.editor}
    //                                                          container={this}/></Provider>, viewsListContent);
}

TemplateModule.prototype.generateToolsBox = function (type, info) {

};


TemplateModule.prototype.updateCliparts = function (cliparts) {
    for (var i = 0; i < cliparts.length; i++) {

        let obrazek = cliparts[i];


        var projectImage = new ProjectImage(obrazek.uid, obrazek._id);
        projectImage.editor = this.editor;
        projectImage.imageUrl = obrazek.imageUrl;
        this.editor.userProject.addClipart(projectImage);
        projectImage.initForUser(null, EDITOR_ENV.staticUrl + obrazek.minUrl, EDITOR_ENV.staticUrl + obrazek.thumbnail, obrazek.trueWidth, obrazek.trueHeight, obrazek.width, obrazek.height, this.editor.userProject.getImageCounter());

        // TODO: cliparts to react!!!
        // document.body.querySelector('#clipartsList').appendChild(projectImage.html);

        //Editor.webSocketControllers.userProject.addPhoto( projectImage.uid, Editor.userProject.getID(), files[actualFile].name, 'Bitmap', null, null, null, projectImage.width, projectImage.height, projectImage.trueWidth, projectImage.trueHeight );

    }

}

TemplateModule.prototype.generateAttributesTool = function () {
    // var Editor = this.editor;
    // var tool = document.createElement('div');
    // tool.id = 'attributes-tool';
    // tool.className = 'tool closed';
    //
    // var toolButton = document.createElement('span');
    // toolButton.id = 'attributes-container-tool_button';
    // toolButton.className = 'tool-button';
    //
    // toolButton.setAttribute('data-content', 'attributes-content');
    //
    // tool.appendChild(toolButton);
    //
    // var toolContent = document.createElement('div');
    // toolContent.id = 'attributes-content';
    // document.getElementById('toolsContent').appendChild(toolContent);
    //
    // var attributesSelector = document.createElement('div');
    // attributesSelector.id = 'attributesSelector';
    //
    // var attributesOptionGeneration = document.createElement('div');
    // attributesOptionGeneration.id = 'attributesOptionGeneration';
    // attributesOptionGeneration.innerHTML = 'Dostosuj wygląd edytora względem cech:';
    //
    // toolContent.appendChild(attributesSelector);
    //
    // toolContent.appendChild(attributesOptionGeneration);
    // document.getElementById('toolsContent').appendChild(toolContent);
    //
    // // miejsce na atrybuty produktu
    // var productAttributes = document.createElement('div');
    // productAttributes.id = 'product-attributes';
    // toolContent.appendChild(productAttributes);
    //
    // // miejsce na baze widoku
    // var baseViewLayer = document.createElement('div');
    // baseViewLayer.id = 'baseViewLayer';
    // toolContent.appendChild(baseViewLayer);
    //
    // var toolHelper = document.createElement('span');
    // toolHelper.className = 'toolHelper';
    // toolHelper.innerHTML = '<i></i><span>Tutaj możesz definiować wygląd edytora poprzez atrybuty produktu</span>';
    //
    // tool.appendChild(toolHelper);
    //
    // var attrConfigViewport = $('#attributes-content');
    //
    // $(attrConfigViewport).children('.viewport').css('height', $('#toolsContent').height() - 60);
    //
    //
    // Ps.initialize(toolContent);
    //
    // return tool;
}


/**
 * Generuje cały wygląd edytora
 *
 * @method generateEditor
 */
TemplateModule.prototype.generateEditor = function (info, type) {

    if (info === 'complex') {
        // tutaj beda ify na to czy edytor jest zaawansowany
        generateComplexToolsBox();
    } else if (info === 'simple') {
        const root = createRoot($('#root')[0])

        root.render(
            <Provider store={store}>
                <TopMenu editor={editor}/>
                <ToolsBox editor={editor} type={type} info={info}/>
                <CarouselBox editor={editor} container={this}/>
                {/*<CanvasTools />*/}
                <div id={"modalsContainer"}>
                    <HeaderInfoModal />
                    <HeaderVideosModal />
                    <RemoveAllImagesModal editor={editor}/>
                    <RemoveSinglePhotoModal editor={editor}/>
                </div>
            </Provider>
        )
        this.generateUserViewsAndThemes()
        this.initToolBoxEvents();
    }
    //generateThemes( info.themes );

};

/**
 * Generuje element motywów
 *
 * @method generateThemes
 * @param {Array} themes Tablica obiektów motywów
 */
TemplateModule.prototype.generateThemes = function (themes) {
};


/**
 * Generuje narzędzie dodawania zdjęć z pamięci komputera
 *
 * @method generateUploadButtons
 * @param {String} type Typ uploadButtons pro|ama
 */
TemplateModule.prototype.generateUploadButtons = function (uploadFunc) {
};

TemplateModule.prototype.imageViewer = function (imageUrl) {

    var elem = document.createElement('div');
    elem.className = 'imageViewerBackground';

    var image = new Image();

    image.onload = function () {

        elem.appendChild(image);

        elem.querySelector('img').style.top = (window.innerHeight - image.offsetHeight) / 2 + 'px';
        elem.querySelector('img').style.left = (window.innerWidth - image.offsetWidth) / 2 + 'px';

    }

    image.src = imageUrl;

    elem.addEventListener('click', function (e) {

        e.stopPropagation();

        elem.parentNode.removeChild(elem);

    });

    document.body.appendChild(elem);

};

/**
 * Generuje narzędzie kontenera obrazków
 *
 * @method generateImagesTool
 * @param {String} type Typ toolsBoxa pro|ama
 */
TemplateModule.prototype.generateImagesTool = function (type) {
    return (
        <div id={"image-container-tool"} className={'tool closed'}>
            <ImagesToolContent editor={this.editor}/>
            <ImagesToolContainer/>
        </div>
    )
};


TemplateModule.prototype.projectImageUploader = function (uploadFunction) {

    var uploader = document.createElement('input');
    uploader.type = 'file';
    uploader.multiple = 'true';
    uploader.className = 'button-fw inputHidden absolutePos';

    uploader.onchange = function (e) {

        var files = this.files; // FileList object

        uploadFunction(files);

    };

    return uploader;

};

TemplateModule.prototype.imageLoader = function (dropBox) {
    var Editor = this.editor;
    if (dropBox) {

        dropBox.addEventListener('drop', function (e) {

            e.stopPropagation();
            e.preventDefault();

            Editor.services.userImagesUpload(e.dataTransfer.files);

        });
    }
};


TemplateModule.prototype.createDragArea = function (element) {

    var imageDrop = document.createElement("DIV");
    imageDrop.id = 'imageDrop';
    imageDrop.dataset.type = "image";
    imageDrop.className = "imageDrop";


    if (element) {
        element.appendChild(imageDrop);
    }

    this.editor.template.imageLoader(imageDrop);


    imageDrop.addEventListener('drop', function (e) {

        e.stopPropagation();
        $('#imageDrop').remove();

    });

    imageDrop.addEventListener('dragleave', function (e) {

        e.stopPropagation();
        $('#imageDrop').remove();

    });


};


/**
 * Generuje box rozszerzający narzędzia
 *
 * @method generateExtendedBoxMenu
 * @param {String} identify Typ ExtendedTopBox pro|ama
 */

var generateExtendedBoxMenu = function (identify, editor) {

    editor.services.calculatePrice();

    var extendedBoxMenu = document.createElement('div');
    var boxContent = document.createElement('div');
    var borderFx = document.createElement('div');

    extendedBoxMenu.id = identify;
    extendedBoxMenu.className = 'extended_box_menu';
    boxContent.className = 'box_menu_content';
    borderFx.className = "border_fx2";

    boxContent.appendChild(borderFx);
    extendedBoxMenu.appendChild(boxContent);

    return extendedBoxMenu;

}

TemplateModule.prototype.displayAllPagesWithPhotos = function () {
    //Cleanup
    var elem = document.body.querySelector('.totalWhitePopUp');
    if (elem) {
        elem.parentNode.removeChild(elem);
    }

    var Editor = this.editor;

    var _this = this;

    var win = document.createElement('div');
    win.className = 'totalWhitePopUp';
    document.body.appendChild(win);

    this.editor.webSocketControllers.userProject.getAllViews(Editor.userProject.getID(), function (project) {

        var currentPage = 0;
        var viewsContainer = document.createElement('div');
        viewsContainer.id = 'viewsContainerPopUp';

        for (var pro = 0; pro < project.projects.length; pro++) {

            let productTypeName = '';

            for (var key in _this.editor.productsNames) {

                if (_this.editor.productsNames[key].indexOf(project.projects[pro].typeID) > -1) {
                    productTypeName = key;
                    break;
                }

            }

            let data = project.projects[pro];

            let projectContainer = document.createElement('div');
            projectContainer.className = 'simple-container';
            projectContainer.setAttribute('simple-id', data._id);

            let productName = document.createElement('div');
            productName.className = 'simple-container-title';
            productName.innerHTML = productTypeName;

            projectContainer.appendChild(productName);

            data.Views = _.sortBy(data.Views, 'order');

            for (var i = 0; i < data.Views.length; i++) {

                var viewElem = document.createElement('div');
                viewElem.setAttribute('data-id', data.Views[i]._id);
                viewElem.className = 'viewElemFromPopUp' + ((data.Views[i].repeatable) ? '' : ' notrepeatable');

                data.Views[i].Pages = _.sortBy(data.Views[i].Pages, 'order');

                var pagesValue = 0;

                for (var pa = 0; pa < data.Views[i].Pages.length; pa++) {

                    pagesValue += data.Views[i].Pages[pa].pageValue;

                }

                viewElem.setAttribute('pages-value', pagesValue);

                for (var p = 0; p < data.Views[i].Pages.length; p++) {

                    var pageElem = document.createElement('div');
                    pageElem.className = 'pageElemFromPopUp';
                    pageElem.setAttribute('data-id', data.Views[i].Pages[p]._id);
                    data.Views[i].Pages[p].UsedImages = _.sortBy(data.Views[i].Pages[p].UsedImages, 'order');
                    data.Views[i].Pages[p].ProposedTemplate.ProposedImages = _.sortBy(data.Views[i].Pages[p].ProposedTemplate.ProposedImages, 'order');

                    var imageContainer = document.createElement("div");
                    imageContainer.className = "imageContainerSortSection";

                    for (var pp = 0; pp < data.Views[i].Pages[p].ProposedTemplate.ProposedImages.length; pp++) {

                        var image = data.Views[i].Pages[p].ProposedTemplate.ProposedImages[pp].objectInside;

                        if (image) {

                            var imageElem = document.createElement('div');
                            imageElem.className = 'imageElemFromPopUp';
                            imageElem.setAttribute('proposed-id', data.Views[i].Pages[p].ProposedTemplate.ProposedImages[pp]._id);
                            imageElem.setAttribute('image-id', image._id);

                            var remover = document.createElement('div');
                            remover.className = 'imageRemover';

                            remover.addEventListener('click', function (e) {

                                e.stopPropagation();

                                var pageID = e.target.parentNode.parentNode.getAttribute('data-id');
                                var imageID = e.target.parentNode.getAttribute('image-id');
                                var proposedPositionID = e.target.parentNode.getAttribute('proposed-id');

                                Editor.webSocketControllers.proposedImage.removeObjectInside(pageID, proposedPositionID);
                                var elem = document.body.querySelector('.totalWhitePopUp');
                                elem.parentNode.removeChild(elem);

                                _this.displayAllPagesWithPhotos();

                            });
                            //Editor.webSocketControllers.userPage.removeUsedImage( editableArea.userPage._id, this.proposedPositionInstance.objectInside.dbID );

                            var imageInside = document.createElement('img');
                            imageInside.src = EDITOR_ENV.staticUrl + image.ProjectImage.thumbnail;
                            imageElem.appendChild(imageInside);
                            imageElem.appendChild(remover);

                            pageElem.appendChild(imageContainer);
                            imageContainer.appendChild(imageElem);

                        } else {

                            var proposedElem = document.createElement('div');
                            proposedElem.className = 'proposedElemPopUp';
                            proposedElem.addEventListener('click', function (e) {

                                e.stopPropagation();

                            });
                            proposedElem.setAttribute('data-id', data.Views[i].Pages[p].ProposedTemplate.ProposedImages[pp]._id);
                            
                            imageContainer.appendChild(proposedElem);
                            pageElem.appendChild(imageContainer);
                        }

                    }

                    var pageNumber = document.createElement('div');
                    pageNumber.className = "pageNumberPopUp";

                    pageNumber.innerHTML = 
                    (currentPage 
                        ? (currentPage + 1 === currentPage + pagesValue 
                            ? (currentPage + 1)  
                            : (currentPage + 1) + '-' + (currentPage + pagesValue)) 
                        : (pagesValue === 1 
                            ? pagesValue 
                            : '1-' + pagesValue)
                    );
                
                    currentPage += pagesValue;

                    pageElem.appendChild(pageNumber);

                    viewElem.appendChild(pageElem);

                    var bottomDiv = document.createElement('div');
                    bottomDiv.className = 'bottomDrag';

                    viewElem.appendChild(bottomDiv);


                    if (data.Views[i].repeatable) {

                        var turnToView = document.createElement('div');
                        turnToView.className = 'seeView';

                        turnToView.addEventListener('click', function (e) {

                            e.stopPropagation();

                            Editor.webSocketControllers.userView.get(e.target.parentNode.parentNode.getAttribute('data-id'), function (data) {

                                win.parentNode.removeChild(win);
                                Editor.userProject.initView(data);

                            });

                        });

                        bottomDiv.appendChild(turnToView);

                        var dragObject = document.createElement('div');
                        dragObject.className = 'dragObjectPopUp';
                        bottomDiv.appendChild(dragObject);

                        var remover = document.createElement('div');
                        remover.className = 'viewRemover';
                        bottomDiv.appendChild(remover);

                        remover.addEventListener('click', function (e) {

                            e.stopPropagation();
                            if (Editor.checkPagesCountConstraint({
                                projectID: e.target.parentNode.parentNode.parentNode.getAttribute('simple-id'),
                                addRemove: 'REMOVE'
                            })) {
                                if (Editor.userProject.isPrevView()) {
                                    Editor.userProject.turnToPreviousView();
                                } else if (Editor.userProject.isNextView()) {
                                    Editor.userProject.turnToNextView();
                                }
                                Editor.webSocketControllers.userProject.removeView(Editor.userProject.getID(), e.target.parentNode.parentNode.parentNode.getAttribute('simple-id'), e.target.parentNode.parentNode.getAttribute('data-id'));
                            }

                        });

                    } else {

                        var turnToView = document.createElement('div');
                        turnToView.className = 'seeView notrepeat';

                        turnToView.addEventListener('click', function (e) {

                            e.stopPropagation();

                            Editor.webSocketControllers.userView.get(e.target.parentNode.parentNode.getAttribute('data-id'), function (data) {

                                win.parentNode.removeChild(win);
                                Editor.userProject.initView(data);

                            });

                        });

                        bottomDiv.appendChild(turnToView);

                    }


                }

                projectContainer.appendChild(viewElem);

            }

            viewsContainer.appendChild(projectContainer);

        }

        var photosContainer = document.createElement('div');
        photosContainer.className = 'photosContainer';

        var photosContainerInner = document.createElement('div');
        photosContainerInner.className = 'photosContainerInner';

        var photosContainerButtons = document.createElement('div');
        photosContainerButtons.className = 'photosContainerButtons';

        var notUsedPhotos = document.createElement('div');
        notUsedPhotos.className = 'notUsedPhotosButton';

        var usedPhotos = document.createElement('div');
        usedPhotos.className = 'usedPhotosButton active';

        var photosContent = document.createElement('div');
        photosContent.className = 'photosContent';

        var leftArrow = document.createElement('div');
        leftArrow.classList = "scrollButton left";

        var rightArrow = document.createElement('div');
        rightArrow.classList = "scrollButton right";

        photosContent.appendChild(leftArrow);
        photosContent.appendChild(photosContainerInner);
        photosContent.appendChild(rightArrow);

        photosContent.addEventListener('click', function (e) {
            e.stopPropagation();
        });

        usedPhotos.addEventListener('click', function (e) {

            e.stopPropagation();

            $(photosContainerInner).removeClass('notUsed');

            $(this).addClass('active');
            $(notUsedPhotos).removeClass('active');

        });

        notUsedPhotos.addEventListener('click', function (e) {

            e.stopPropagation();

            $(photosContainerInner).addClass('notUsed');
            $(this).addClass('active');
            $(usedPhotos).removeClass('active');

        });

        photosContainerButtons.appendChild(notUsedPhotos);
        photosContainerButtons.appendChild(usedPhotos);

        photosContainer.appendChild(photosContainerButtons);
        photosContainer.appendChild(photosContent);

        var images = Editor.userProject.getProjectImages();
        var imagesLength = 0;

        for (var key in images) {

            photosContainerInner.appendChild(images[key].getHTMLForSortingViews());
            imagesLength++;

        }

        //FUNCKJE DO SCROLLOWANIA W KRAUZELI

        leftArrow.addEventListener('click', function() {
            photosContainerInner.scrollBy({
                left: -photosContainerInner.offsetWidth / 2, 
                behavior: 'smooth'
            });
        });
        
        rightArrow.addEventListener('click', function() {
            photosContainerInner.scrollBy({
                left: photosContainerInner.offsetWidth / 2,
                behavior: 'smooth'
            });
        });

        photosContainerInner.addEventListener('wheel', function(event) {
            const scrollableContainer = event.currentTarget; 
            scrollableContainer.scrollLeft += event.deltaY;
            event.preventDefault(); 
        })


        win.appendChild(viewsContainer);
        win.appendChild(photosContainer);

        // photosContainerInner.style.width = imagesLength * 104 + 'px';
        // photosContainerInner.style.height = photosContainer.offsetHeight + 'px';

        function closeWin(e) {

            e.stopPropagation();
            win.parentNode.removeChild(win);

        }

        var windowCloser = document.createElement('div');
        windowCloser.className = 'windowCloser';
        windowCloser.addEventListener('click', closeWin);

        win.appendChild(windowCloser);

        //win.addEventListener('click', closeWin );

        $('.photoElemPopUp').on('click', function (e) {

            e.stopPropagation();

        });

        $('.photoElemPopUp').draggable(
            {
                appendTo: 'body',
                start: function (event, ui) {

                    event.stopPropagation();
                    //win.removeEventListener( 'click', closeWin );
                    $('.proposedElemPopUp').addClass('prepareToDrop');
                    $('.imageElemFromPopUp').append('<div class="dropLayer"></div>');

                },
                stop: function (event, ui) {

                    event.stopPropagation();

                    if ($(event.originalEvent.target).hasClass('dropLayer')) {

                        var projectImageUID = event.target.getAttribute('data-uid');
                        var proposedPositionID = event.originalEvent.target.parentNode.getAttribute('proposed-id');
                        var pageID = event.originalEvent.target.parentNode.parentNode.getAttribute('data-id');

                        Editor.webSocketControllers.proposedImage.changeImage(proposedPositionID, projectImageUID, pageID);

                    } else {

                        var projectImageUID = event.target.getAttribute('data-uid');
                        var proposedPositionID = event.originalEvent.target.getAttribute('data-id');
                        var pageID = event.originalEvent.target.parentNode.getAttribute('data-id');
                        Editor.webSocketControllers.proposedImage.loadImage(proposedPositionID, projectImageUID, pageID);

                    }

                    $('.proposedElemPopUp').removeClass('prepareToDrop');
                    $('.imageElemFromPopUp').each(function () {

                        $(this).children('.dropLayer').remove();

                    });
                    var elem = document.body.querySelector('.totalWhitePopUp');
                    elem.parentNode.removeChild(elem);

                    _this.displayAllPagesWithPhotos();
                },
                opacity: 0.7,
                helper: "clone",
                cursorAt: {left: -20, top: -20}
            }
        );

        $('.simple-container').sortable({

            items: '> div.viewElemFromPopUp:not(.notrepeatable)',

            stop: function (event) {

                event.stopPropagation();
                var sortedObjects = $(this).sortable("toArray", {attribute: 'data-id'});

                var firstSortElemAttribute = sortedObjects[0];
                var childs = this.childNodes;
                var notRepeatableBefore = 0;

                for (var i = 1; i < childs.length; i++) {

                    if (childs[i].getAttribute('data-id') == firstSortElemAttribute) {

                        break;

                    } else {

                        notRepeatableBefore++;

                    }

                }

                var sortTable = [];

                for (var i = 0; i < sortedObjects.length; i++) {

                    var sortObject = {

                        viewID: sortedObjects[i],
                        order: notRepeatableBefore + i

                    };

                    sortTable.push(sortObject);

                }

                var _views = Editor.userProject.getViews();

                // lokalna aktualizacja orderw, powinna byc po otrzymaniu callbackow...
                for (var i = 0; i < sortTable.length; i++) {

                    var newViewsOrder = sortTable[i];

                    var view = _views.find((v) => v._id === newViewsOrder.viewID);
                    if (!view) {
                        console.error('Nie ma widoku')
                    } else {
                        view.order = newViewsOrder.order;
                    }
                }

                Editor.userProject.sortViews();
                // sortowanie, ale w obrębie danego projektu
                Editor.webSocketControllers.userProject.setViewsOrders($(this).attr('simple-id'), sortTable);
                var elem = document.body.querySelector('.totalWhitePopUp');
                elem.parentNode.removeChild(elem);

                _this.displayAllPagesWithPhotos();
            }

        });

        /*
        $('.pageElemFromPopUp').sortable({

            connectWith: ".pageElemFromPopUp",
            items: '> *:not(.pageNumberPopUp)',

            stop : function( event, ui ){

                if( event.target.parentNode.hasClass('notrepeatable') && event.target.children.length-1 == 2 ){

                    $(this).sortable("cancel");

                }else {

                    event.stopPropagation();
                    console.log( event.target );
                    console.log( event.originalEvent.target.parentNode );
                    console.log('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=');

                }


            },


        });
        */

    });

}

TemplateModule.prototype.resizeToUserObject = function (obj) {

    var scaleX = 1;
    var scaleY = 1;
    var tmpX = this.editor.getStage().scaleX;
    var tmpY = this.editor.getStage().scaleY;
    var margin = 110;
    var offset = 80;
    var offsetX = 431 + 80; //pasek z boku (nasze menu narzędzi) + przycisk zmiany pozycji proponowanych

    if (document.getElementById('viewsListUser').getAttribute('isopen') == 'true' || document.getElementById('pagesListUser').getAttribute('isopen') == 'true') {

        var offsetY = margin + parseInt($('#viewsListUser').height()); //105 rozmiar paska na dole + przyciski zmiany stron

    } else {

        if (parseInt($('#viewsListUser').css('bottom')) > parseInt($('#pagesListUser').css('bottom'))) {

            var offsetY = margin + parseInt($('#viewsListUser').height()) + parseInt($('#viewsListUser').css('bottom'))

        } else {

            var offsetY = margin + parseInt($('#pagesListUser').height()) + parseInt($('#pagesListUser').css('bottom'))

        }

    }

    var destinationMaxWidth = this.editor.getCanvas().width() - offsetX;
    var destinationMaxHeight = this.editor.getCanvas().height() - offsetY;

    var newScale = destinationMaxWidth / this.editor.getStage().getBounds().width;

    if (destinationMaxHeight < (this.editor.getStage().getBounds().height * newScale)) {

        newScale = destinationMaxHeight / this.editor.getStage().getBounds().height;

    }

    this.editor.getStage().scaleX = newScale;
    this.editor.getStage().scaleY = newScale;

    this.editor.stage.centerCameraXuser();
    this.editor.stage.centerCameraYuser();

};

export {TemplateModule};

//Editor.template.alertFunction();
