import React from "react";
import {ProjectNameComponent} from "../ProjectNameComponent";
import {connect} from 'react-redux';
import {
    changeFullScreenMode,
    setEditorType
} from "../../redux/reducers/project/project";
import {setActiveToolIndex} from "../../redux/reducers/toolsbox/toolsBox";
import toolsList from "../toolsBox/ToolsList";
import SelectedImageTools from "./components/SelectedImageTools";
import SelectedTextTools from "./components/SelectedTextTools";
import HeaderButton from "./components/HeaderButton";
import DropdownOnHover from "../../components/DropdownOnHover";
import Slider from "../../components/Slider";
import {setEditingImageEffects, setEditingImagePosition} from "../../redux/reducers/images/selectedImage";
import ZoomIn from "../../components/ZoomIn";
import ZoomOut from "../../components/ZoomOut";


// Generating editor header
class TopMenu extends React.Component {

    constructor(props) {
        super(props);
        this.editor = props.editor;
        this.editorType = props.editorType;

        this.state = {
            price: 0,
            fullScreen: this.editor.fullScreenMode,
            zoomValue: this.editor.getStage().scaleX,
            min: this.editor.getStage().scaleX,
            max: this.editor.getStage().scaleX + 4,
            step: 0.01,
        }
    }

    componentDidMount() {
        window.addEventListener('resize', this.updateZoomOnResize);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateZoomOnResize);
    }


    updateStateParam(param, value) {

        var currentState = JSON.parse(JSON.stringify(this.state));
        currentState[param] = value;
        this.setState(currentState);

    }

    saveProject() {

        var projectID = this.editor.userProject.getID();
        //TODO Make it working| you could also forgot about this /j

        $.get( EDITOR_ENV.frameworkUrl + '/pdfGenerating/?projectID='+projectID, function( data ){

            alert('Projekt został zapisany, mozesz do niego powórcić w przyszłości');

        }.bind(this));
    }

    checkout() {

        var projectID = this.editor.userProject.getID();
        /*
        $.get( EDITOR_ENV.frameworkUrl + '/pdfGenerating/?projectID='+projectID, function( data ){

        }.bind(this));
        */

        this.editor.services.addToCart();

    }

    // someday it needs to be moved to the separated file
    showFlipBook(e) {
        e.stopPropagation();
        var pages = this.editor.userProject.getOrderedPages();

        for (var key = 0; key < pages.length; key++) {

            if (pages[key].prev) {

            } else {

                alert('podgląd stron jest jeszcze nie gotowy, spróbuj ponownie za parę sekund');

                return false;
            }

        }

        var cover = this.editor.userProject.getCoverPage();

        for (var key = 0; key < cover.length; key++) {

            if (cover[key].prev) {

            } else {

                alert('podgląd okładki jest jeszcze nie gotowy, spróbuj ponownie za parę sekund');

                return false;
            }

        }
        var flipbookHolder = document.createElement('div');
        flipbookHolder.className = 'flipbook-holder';

        var remove = document.createElement('div');
        remove.className = 'remove-flipbook';
        remove.innerHTML = 'x';

        flipbookHolder.appendChild(remove);

        document.body.appendChild(flipbookHolder);

        var nextPage = document.createElement('div');
        nextPage.className = 'nextPage-flipbook';
        var prevPage = document.createElement('div');
        prevPage.className = 'prevPage-flipbook';

        prevPage.addEventListener('click', function (e) {

            e.stopPropagation();

            $("#flipbook").turn("previous");

        });

        nextPage.addEventListener('click', function (e) {

            e.stopPropagation();

            $("#flipbook").turn("next");

        });

        var html = '<div id="flipbook">';
        if (cover.length > 0 && cover[0].prev.length > 0) {
            html += `<div class="hard first"><img src="${cover[0].prev[0]}"></div><div class="hard"></div>`;
        }
        html += ''

        var pages = this.editor.userProject.getOrderedPages();
        for (var key = 0; key < pages.length; key++) {

            if (pages[key] && pages[key].prev) {
                for (var i = 0; i < pages[key].prev.length; i++) {
                    html += '<div class=""><img src="' + pages[key].prev[i] + '"></div>';
                }
            } else {
                html += '<div class="not-loaded"></div>';
            }

        }

        html += '';
        if (cover.length > 0 && cover[0].prev.length > 0) {
            html += `<div class="hard"></div><div class="hard last"><img src="${cover[0].prev[0]}"></div>`;
        }
        html += '</div>';

        flipbookHolder.innerHTML += html;

        var width = window.innerWidth * 0.6;
        var aspect = width / this.editor.userProject.getBookFormat().width;
        var height = this.editor.userProject.getBookFormat().height * aspect;

        if (height > window.innerHeight) {

            height = window.innerHeight * 0.7;
            aspect = height / this.editor.userProject.getBookFormat().height;
            width = this.editor.userProject.getBookFormat().width * aspect;
        }

        flipbookHolder.style.paddingTop = (height - window.innerHeight) / 2 + "px";

        $("#flipbook").turn({
            height: height,
            width: width,
            autoCenter: true
        });

        $('.remove-flipbook').on('click', function (e) {

            e.stopPropagation();
            $(this).parent().remove();

        });


        flipbookHolder.appendChild(nextPage);
        flipbookHolder.appendChild(prevPage);

    }

    toggleEditorMode() {
        const {
            setEditorType,
            setActiveToolIndex,
        } = this.props

        const { editorType, activeToolIndex } = this.props

        if (editorType === 'user') {
            const newType = "advancedUser";

            $("#orderPrice").animate({
                    width: 0,
                    opacity: 0
                }, 300, () => {
                    $("#orderPrice").hide()

                    setEditorType(newType)
                    this.editor.userType = userType = newType;
                    //addEditorConfiguration.className = "editor_configuration top_menu_icons";

                    this.editor.userProject.redrawView();
                    const stage = Editor.getStage();
                    const initialZoom = stage.scaleX - (0.18 * Math.log(stage.scaleX));

                    this.setState({
                        zoomValue: initialZoom,
                        minZoom: initialZoom,
                        maxZoom: initialZoom + 2,
                    });
                }
            )
        } else {
            const newType = "user";

            // prevent displaying advanced active tool in toolsbox
            setActiveToolIndex(toolsList[activeToolIndex].type === "advanced" ? toolsList.filter(tool => tool.type === "simple").length - 1 : activeToolIndex);
            setEditorType(newType)
            this.editor.userType = userType = newType;

            //addEditorConfiguration.className = "editor_configuration simple top_menu_icons";

            this.editor.userProject.redrawView();

            this.setState({
                isDropdownVisible: false,
                zoomValue: null,
                minZoom: null,
                maxZoom: null,
            });

            $("#orderPrice")
                .show()
                .animate({
                    width: "100%",
                    opacity: 1,
                    transformOrigin: "left"
                }, 300)
        }
    }

    handleSliderChange = (v) => {
        const value = parseFloat(v);

        this.setState({ zoomValue: value }, () => {
            this.updateStageZoom(value); // Zaktualizuj scenę po zmianie stanu
        });
    };

    updateZoomOnResize = () => {
        const stage = Editor.getStage();
        const newZoom = stage.scaleX;

        this.setState({
            zoomValue: newZoom,
            minZoom: newZoom,
            maxZoom: newZoom + 4,
        });
    };

    updateStageZoom = (value) => {
        const stage = Editor.getStage();
        stage.scaleX = value;
        stage.scaleY = value;
        Editor.stage.redrawRulers();
        Editor.stage.updateNetHelper();

        // Dispatching event
        const zoomEvent = new createjs.Event("stageScroll");
        Editor.stage.dispatchEventForAllObject(zoomEvent);

        // Optional: Center camera for "user" type
        if (userType === 'user') {
            const mainLayerSize = Editor.stage.getMainLayer().getTransformedBounds();
            const area = Editor.stage.getVisibleAreaSize();

            if (area.width > mainLayerSize.width) {
                Editor.stage.centerCameraX();
            }
            if (area.height > mainLayerSize.height) {
                Editor.stage.centerCameraY();
            }
        }
    };

    fullScreenOff() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }

        this.props.changeFullScreenMode(false);
    }

    fullScreenOn() {
        const element = document.documentElement;

        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }

        this.props.changeFullScreenMode(true);
    }

    isAdvancedMode = () => {
        return ['advancedUser', 'advancedAdmin'].some(c => c === this.props.editorType)
    }

    render() {
        const {selectedImage, text, editorType, fullScreenMode} = this.props;

        return (
            <div id={"top-menu"} className={'displayController'}>
                <ProjectNameComponent editor={this.editor} />
                <div className={'navigation-wrapper'}>

                    <div className={'navigation-container'}>
                        <HeaderButton className={'backwards disabled'}/>
                        <HeaderButton className={'forwards'}/>

                        {selectedImage.active && <SelectedImageTools />}
                        {text.active && <SelectedTextTools editor={this.editor} />}
                    </div>
                    <div className={'navigation-container'}>
                        {editorType === "advancedUser" && (
                            <>
                                <div className={'slider-container'}>
                                    <ZoomOut
                                        {...this.state}
                                        value={this.state.zoomValue}
                                        handleOnClick={this.handleSliderChange}
                                    />
                                    <Slider
                                        {...this.state}
                                        value={this.state.zoomValue}
                                        handleOnChange={this.handleSliderChange}
                                    />
                                    <ZoomIn
                                        {...this.state}
                                        value={this.state.zoomValue}
                                        handleOnClick={this.handleSliderChange}
                                    />
                                    <DropdownOnHover
                                        elements={[
                                            {
                                                element: <HeaderButton
                                                    className={'fullscreen in-dropdown'}
                                                />,
                                                title: "Tryb pełnoekranowy",
                                                description: "Umożliwia przełączenie widoku obszaru roboczego na pełny ekran.",
                                                onClick: this.fullScreenOn.bind(this)
                                            },
                                            {element: <HeaderButton className={'ruler in-dropdown'}/>, title: "Magnetyczne przyciąganie", description: "Automatyczne przyciąganie elementów do linii pomocniczych w obszarze roboczym."},
                                            {element: <HeaderButton className={'magnet in-dropdown'} />, title: "Siatka", description: "Włącza widoczną siatkę na obszarze roboczym, pomagając w precyzyjnym układaniu elementów."}
                                        ]}
                                    >
                                        <HeaderButton className={'burger'}/>
                                    </DropdownOnHover>
                                </div>
                            </>
                        )}

                        <div className={"navigation-actions-buttons-container"}>
                            <HeaderButton
                                className={'info-button navigation-modal-button'}
                                data-bs-toggle={"modal"}
                                data-bs-target={"#infoModal"}
                            />
                            <HeaderButton
                                className={'editor-manual-button navigation-modal-button'}
                                data-bs-toggle={"modal"}
                                data-bs-target={"#videosModal"}
                            />
                            {fullScreenMode && !this.isAdvancedMode() && (
                                <HeaderButton
                                    className={'fullscreen'}
                                    onClick={this.fullScreenOff.bind(this)}
                                />
                            )}
                            <HeaderButton
                                className={'flipbook'}
                                onClick={(e) => this.showFlipBook(e)}
                            />
                            <HeaderButton
                                className={`settings-button ${this.isAdvancedMode() ? "advanced" : ""}`}
                                onClick={this.toggleEditorMode.bind(this)}
                            />
                            <HeaderButton
                                className={'save-button'}
                                onClick={this.saveProject.bind(this)}
                            />
                        </div>
                        <HeaderButton
                            className={`cart-button ${this.isAdvancedMode() ? "only-icon" : ""}`}
                            onClick={this.checkout.bind(this)}
                        >
                            <span id={"orderPrice"}>...</span>
                        </HeaderButton>
                    </div>
                </div>
            </div>
        );

    }
}

const mapStateToProps = (state) => ({
    ...state.projectReducer,
    ...state.selectedImageReducer,
    ...state.toolReducer
});

const mapDispatchToProps = {
    setEditorType,
    setEditingImageEffects,
    setEditingImagePosition,
    setActiveToolIndex,
    changeFullScreenMode
};

export default connect(mapStateToProps, mapDispatchToProps)(TopMenu);