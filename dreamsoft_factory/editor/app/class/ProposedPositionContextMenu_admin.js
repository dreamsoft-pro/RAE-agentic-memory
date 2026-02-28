import ContextMenuTools from "./ContextMenuTools";
import {RANGE} from '../Editor'
import {ProposedPosition2} from "./ProposedPosition2";

var generateFlatSwitch = function (selected) {

    var flatSwitch = document.createElement('div');

    flatSwitch.className = "block-switch";
    flatSwitch.innerHTML = '<input id="custom-toggle-flat-border" class="custom-toggle custom-toggle-flat" type="checkbox" ' + ((selected) ? 'checked="checked"' : '') + ' >' +
        '<label for="custom-toggle-flat-border"></label>';
    return flatSwitch;

}

/**
 * Klasa reprezentująca menu kontekstowe dla pozycji proponowanej
 *
 * @class ProposedPositionContextMenu
 * @constructor
 */
function ProposedPositionContextMenu(proposedPosition, menuType) {

    this.proposedPositionInstance = proposedPosition;
    this.editor = proposedPosition.editor;
    proposedPosition._toolBox = this;
    proposedPosition.contextMenu = this;
    this.toolsContainer = null;
    this.initAllTools(menuType);
    this._updateToolsBoxPosition();
    this.toolBoxExtend = null;

};


var p = ProposedPositionContextMenu.prototype;


p.layerUp = function () {

    var Editor = this.editor;
    var _this = this.proposedPositionInstance;

    var layerUp = document.createElement('div');
    layerUp.className = 'button';
    layerUp.id = 'layerUpButton';


    layerUp.appendChild(Editor.template.createToolhelper("Warstwa w górę"));


    layerUp.addEventListener('click', function (e) {

        e.stopPropagation();

        var editingObject = _this;

        var index = editingObject.parent.getChildIndex(editingObject);

        // jezeli obiekt znajduje sie w editable area i użytkonik jest aminem
        // Editor.webSocketControllers.themePage.changeObjectsOrder( editingObject.parent.parent );

        // TO DO: jeżeli obiekt ni e jest w editablearea i jest admiem
        if (index < editingObject.parent.children.length - 1) {

            editingObject.parent.setChildIndex(editingObject, index + 1);
            editingObject.order = index + 1;

            var moveDownObject = editingObject.parent.getChildAt(index);
            moveDownObject.order = index;

        }

        var viewLayerInfo = Editor.adminProject.format.view.getLayerInfo();

        Editor.webSocketControllers.userPage.moveObjectUp(_this.dbID, _this.getFirstImportantParent().userPage._id);

    });

    return layerUp;

};


p.layerDown = function () {

    var Editor = this.editor;
    var _this = this.proposedPositionInstance;


    var layerDown = document.createElement('div');
    layerDown.className = 'button';
    layerDown.id = 'layerDownButton';


    layerDown.appendChild(Editor.template.createToolhelper("Warstwa w dół"));

    layerDown.addEventListener('click', function (e) {

        var editingObject = _this;

        var index = editingObject.parent.getChildIndex(editingObject);

        // jezeli obiekt znajduje sie w editable area i użytkonik jest aminem
        // Editor.webSocketControllers.themePage.changeObjectsOrder( editingObject.parent.parent );

        // TO DO: jeżeli obiekt ni e jest w editablearea i jest admiem


        if (index > 0) {

            editingObject.parent.setChildIndex(editingObject, index - 1);

        } else {

            if (editingObject.parent.name == 'foregroundLayer') {

                var background = editingObject.parent.parent.backgroundLayer;
                editingObject.parent.removeChild(editingObject);

                if (background.children.length > 0)
                    background.addChildAt(editingObject, background.children.length - 1);
                else
                    background.addChildAt(editingObject, background.children.length);

            } else {


            }

        }

        var viewLayerInfo = Editor.adminProject.format.view.getLayerInfo();


        Editor.webSocketControllers.userPage.moveObjectDown(_this.dbID, _this.getFirstImportantParent().userPage._id);

    });

    return layerDown;

};


/**
 * Inicjalizuje wszystkie narzędzia i dołącza je do tool boxa
 *
 * @method initAllTools
 */
p.initAllTools = function (menuType) {

    var _this = this;

    var editingObject = this.proposedPositionInstance;
    var Editor = editingObject.editor;

    if (editingObject.borderWidth) {

        if (editingObject.borderWidth == 0) {

            editingObject.unDropBorder();
        }

    }

    var tools = document.createElement("div");
    tools.id = "proposedTemplate-toolsbox";
    tools.className = "tools-box";

    var userTools = document.createElement("div");
    userTools.className = "editorBitmapTools editorBitmapTools6";

    userTools.appendChild(this.layerDown());
    userTools.appendChild(this.layerUp());
    userTools.appendChild(this.createBorderTool());
    userTools.appendChild(this.createBackgroundFrameTool());
    userTools.appendChild(this.createShadowTool());
    userTools.appendChild(this.removeImageTool());

    tools.appendChild(userTools);

    this.toolsContainer = tools;

    this.proposedPositionInstance.addEventListener('move', function (e) {

        _this._updateToolsBoxPosition();

    });

    this.proposedPositionInstance.addEventListener('scale', function (e) {

        _this._updateToolsBoxPosition();

    });

    this.proposedPositionInstance.addEventListener('rotate', function (e) {

        _this._updateToolsBoxPosition();

    });

    this.proposedPositionInstance.addEventListener('resize', function (e) {

        _this._updateToolsBoxPosition();

    });

    document.body.appendChild(tools);
    this.element = tools;

};

p.createBorderTool = function () {

    var _this = this;
    var object = this.proposedPositionInstance;
    var Editor = object.editor;
    var tool = document.createElement('div');
    tool.className = 'button';
    tool.id = 'borderButton';

    tool.appendChild(Editor.template.createToolhelper("Dodaj ramkę do zdjęcia", 'none', 'infoBoxBorder'));

    tool.addEventListener('click', function (e) {

        e.stopPropagation();

        if (_this.openSection == 'border' || _this.openSection != null) {

            _this.toolsContainer.removeChild(_this.currentExtendedTool);

            if (_this.openSection != null) {

                _this.toolsContainer.appendChild(_this.initBorderBoxTool());
                _this._updateToolsBoxPosition();

            } else {

                _this.openSection = null;

            }

        } else {

            _this.toolsContainer.appendChild(_this.initBorderBoxTool());
            _this._updateToolsBoxPosition();

        }

    });

    return tool;
};

p.initBorderBoxTool = function () {

    var elem = document.createElement('div');
    elem.className = 'toolBoxExtend';

    var globalSettings = document.createElement('div');
    globalSettings.className = 'toolBoxExtendSection';

    var title = document.createElement('div');
    title.className = 'title';
    title.innerHTML = 'Włącz ramkę:';

    var singleElem = document.createElement('div');
    singleElem.className = 'button singleElem active';

    var singleElemImage = new Image();
    singleElemImage.src = 'images/1zdjecie-on.svg';

    singleElem.appendChild(singleElemImage);

    var allElemInPage = document.createElement('div');
    allElemInPage.className = 'button allElemInPage';

    var allElemInPageImage = new Image();
    allElemInPageImage.src = "images/1strona-on.svg";

    allElemInPage.appendChild(allElemInPageImage);

    var info = document.createElement('div');
    info.className = 'buttonsSettingsInfo';
    info.innerHTML = 'Dla aktualnego zdjęcia';


    globalSettings.appendChild(title);
    globalSettings.appendChild(singleElem);
    globalSettings.appendChild(allElemInPage);
    globalSettings.appendChild(info);

    var valuesSettings = document.createElement('div');
    valuesSettings.className = 'toolBoxExtendSection';

    var borderWidthPickerLabel = document.createElement('label');
    borderWidthPickerLabel.className = 'borderToolsClass inputRight';
    borderWidthPickerLabel.innerHTML = "Grubość ramki:";

    var borderWidthPickerInputUser = document.createElement("input");
    borderWidthPickerInputUser.className = 'spinner';
    borderWidthPickerInputUser.value = this.proposedPositionInstance.borderWidth;

    borderWidthPickerLabel.appendChild(borderWidthPickerInputUser);

    var borderColor = document.createElement('input');
    borderColor.id = 'borderColor';
    borderColor.className = 'spinner cp-full';

    function changeInRange() {
        if (curentRange == RANGE.singleElem) {
            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            editingObject.setBorderWidth(width);
            editingObject.updateSimpleBorder();
            editingObject.setBorderColor(color);

        } else if (curentRange == RANGE.allElemInPage) {
            Editor.getEditableObjectsByType(RANGE.allElemInPage, 'ProposedPosition')
                .forEach((eo) => {
                    eo.setBorderWidth(width);
                    eo.updateSimpleBorder();
                    eo.setBorderColor(color);
                });
        }
    }

    let curentRange = RANGE.singleElem

    singleElem.addEventListener('click', function (e) {

        e.stopPropagation();

        if (!$(this).hasClass('active')) {

            $(allElemInPage).removeClass('active');
            $(singleElem).addClass('active');
            info.innerHTML = 'Dla aktualnego zdjęcia';
            curentRange = RANGE.singleElem
            changeInRange()
        }

    });

    allElemInPage.addEventListener('click', function (e) {

        e.stopPropagation();

        if (!$(this).hasClass('active')) {

            $(singleElem).removeClass('active');
            $(allElemInPage).addClass('active');
            info.innerHTML = 'Dla wszystkich zdjęć na stronie';
            curentRange = RANGE.allElemInPage
            changeInRange()
        }

    });

    let width = this.proposedPositionInstance.borderWidth
    $(borderWidthPickerInputUser).spinner({

        min: 0,

        spin: function (event) {
            width = parseInt(event.target.value)
            changeInRange();

        },
        change: function (event) {

            width = parseInt(event.target.value)
            changeInRange();

        },

        stop: function (event) {

            width = parseInt(event.target.value)
            changeInRange();

        }

    }).val(width);


    var borderColorPicker = document.createElement('div');
    borderColorPicker.className = 'borderColorPicker';

    var borderColorPickerLabel = document.createElement('h4');
    borderColorPickerLabel.className = 'borderColorPickerLabel';

    var borderColor = document.createElement('input');
    borderColor.id = 'borderColor';
    borderColor.className = 'spinner cp-full';

    borderColorPicker.appendChild(borderColorPickerLabel);
    borderColorPickerLabel.appendChild(borderColor);
    let color = this.proposedPositionInstance.borderColor
    $(borderColor).val(color).colorpicker({

        parts: 'full',
        showOn: 'both',
        buttonColorize: true,
        showNoneButton: true,
        alpha: true,
        color: color,
        stop: function (e) {
            color = e.target.value
            changeInRange()

        },
        select: function (e) {

            color = e.target.value
            changeInRange()

        },

        colorFormat: 'RGBA'

    });

    valuesSettings.appendChild(borderWidthPickerLabel);
    valuesSettings.appendChild(borderColorPickerLabel);

    elem.appendChild(globalSettings);
    elem.appendChild(valuesSettings);

    this.currentExtendedTool = elem;
    this.openSection = 'border';

    return elem;

};

p.createBackgroundFrameTool = function () {

    var object = this.proposedPositionInstance;
    var Editor = object.editor;
    var _this = this;

    var tool = document.createElement('div');
    tool.className = 'button';
    tool.id = 'backframeButton';

    tool.appendChild(Editor.template.createToolhelper("Dodaj ramkę do zdjęcia", 'none', 'infoBoxBorder'));
    tool.addEventListener('click', function (e) {

        e.stopPropagation();

        if (_this.openSection == 'backframe' || _this.openSection != null) {
            //console.log( _this.currentExtendedTool );
            //console.log( _this.toolsContainer );
            _this.toolsContainer.removeChild(_this.currentExtendedTool);

            if (_this.openSection != null) {

                _this.toolsContainer.appendChild(_this.initBackframeBoxTool($(_this.toolsContainer).width()));
                _this._updateToolsBoxPosition();

            } else {

                _this.openSection = null;

            }

        } else {

            _this.toolsContainer.appendChild(_this.initBackframeBoxTool($(_this.toolsContainer).width()));
            _this._updateToolsBoxPosition();

        }

    });

    return tool;
};

p.initBackframeBoxTool = function (width) {
    let backgroundFrame = this.proposedPositionInstance.backgroundFrame
    let backgroundFrameID = this.proposedPositionInstance.backgroundFrameID

    let curentRange = RANGE.singleElem

    function changeInRange() {
        if (curentRange == RANGE.singleElem) {
            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.backgroundFrame = backgroundFrame;
            if (backgroundFrame) {
                Editor.webSocketControllers.frameObject.get(backgroundFrameID, function (data) {
                    editingObject.setBackgroundFrame(data);
                });
            } else {
                editingObject.removeBackgroundFrame();
            }
        } else if (curentRange == RANGE.allElemInPage) {
            if (backgroundFrame) {
                Editor.webSocketControllers.frameObject.get(backgroundFrameID, function (data) {
                    Editor.getEditableObjectsByType(RANGE.allElemInPage, 'ProposedPosition')
                        .forEach((eo) => {
                            eo.backgroundFrame = backgroundFrame;
                            eo.setBackgroundFrame(data);
                        });
                });

            }else{
                Editor.getEditableObjectsByType(RANGE.allElemInPage, 'ProposedPosition')
                    .forEach((eo) => {
                        eo.backgroundFrame = backgroundFrame;
                        eo.removeBackgroundFrame();
                    });
            }
        }
    }

    this.openSection = 'backframe';
    var elem = this.currentExtendedTool = document.createElement('div');
    elem.className = 'toolBoxExtend';
    elem.style.width = width + 'px';

    var globalSettings = document.createElement('div');
    globalSettings.className = 'toolBoxExtendSection';

    var title = document.createElement('div');
    title.className = 'title';
    title.innerHTML = 'Włącz tylną ramkę:';

    var singleElem = document.createElement('div');
    singleElem.className = 'button singleElem active';

    singleElem.addEventListener('click', function (e) {

        e.stopPropagation();

        if (!$(this).hasClass('active')) {

            $(allElemInPage).removeClass('active');
            $(singleElem).addClass('active');
            info.innerHTML = 'Dla aktualnego zdjęcia';
            curentRange=RANGE.singleElem
            changeInRange()
        }

    });

    var singleElemImage = new Image();
    singleElemImage.src = 'images/1zdjecie-on.svg';

    singleElem.appendChild(singleElemImage);

    var allElemInPage = document.createElement('div');
    allElemInPage.className = 'button allElemInPage';

    allElemInPage.addEventListener('click', function (e) {

        e.stopPropagation();

        if (!$(this).hasClass('active')) {

            $(singleElem).removeClass('active');
            $(allElemInPage).addClass('active');
            info.innerHTML = 'Dla wszystkich zdjęć na stronie';
            curentRange=RANGE.allElemInPage
            changeInRange()
        }

    });

    var allElemInPageImage = new Image();
    allElemInPageImage.src = "images/1strona-on.svg";

    allElemInPage.appendChild(allElemInPageImage);

    var info = document.createElement('div');
    info.className = 'buttonsSettingsInfo';
    info.style = 'clear:both'
    info.innerHTML = 'Dla aktualnego zdjęcia';

    var onOffLabel = document.createElement('label');
    var onOff = document.createElement('input');
    onOff.type = 'checkbox';
    onOff.className = 'switch';
    onOff.checked = (this.proposedPositionInstance.backgroundFrame) ? true : false;
    onOff.addEventListener('change', function (e) {

        backgroundFrame = e.target.checked
        changeInRange()

    });

    var onOffDispl = document.createElement('div');

    onOffLabel.appendChild(onOff);
    onOffLabel.appendChild(onOffDispl);

    globalSettings.appendChild(title);
    globalSettings.appendChild(onOffLabel);

    const rangeSelectorsLayer = document.createElement('div');
    rangeSelectorsLayer.style = 'float:left'
    globalSettings.appendChild(rangeSelectorsLayer);

    rangeSelectorsLayer.appendChild(singleElem);
    rangeSelectorsLayer.appendChild(allElemInPage);
    rangeSelectorsLayer.appendChild(info);

    var firstSection = document.createElement('div');
    firstSection.className = 'toolBoxExtendSection';
    firstSection.appendChild(globalSettings);

    var secondSection = document.createElement('div');
    secondSection.className = 'toolBoxExtendSection'

    var framesContainer = document.createElement('div');
    framesContainer.className = 'backgroundFramesContainer contentSlider';
    framesContainer.style.width = (width - 25) + 'px';

    var framesInner = document.createElement('div');
    framesContainer.appendChild(framesInner);

    var framesContainerLeftArrow = document.createElement('div');
    framesContainerLeftArrow.className = 'leftArrow-cont';
    framesContainerLeftArrow.addEventListener('click', function (e) {

        e.stopPropagation();
        if (framesContainer.scrollLeft > 0) {

            if (framesContainer.scrollLeft < 0) {

                framesContainer.scrollLeft = 0;

            }

        }

    });

    var framesContainerRightArrow = document.createElement('div');
    framesContainerRightArrow.className = 'rightArrow-cont';
    framesContainerRightArrow.addEventListener('click', function (e) {

        e.stopPropagation();
        if (framesContainer.scrollLeft < (parseInt($(framesInner).width()) - (width - 25))) {

            framesContainer.scrollLeft += 102;

            framesContainer.scrollLeft -= 102;

            if (framesContainer.scrollLeft > (parseInt($(framesInner).width()) - (width - 25))) {

                framesContainer.scrollLeft = (parseInt($(framesInner).width()) - (width - 25));

            }

        }

    });

    var framesContainerParent = document.createElement('div');
    framesContainerParent.style.width = (width - 20) + 'px';
    framesContainerParent.style.position = 'relative';

    framesContainerParent.appendChild(framesContainerLeftArrow);
    framesContainerParent.appendChild(framesContainerRightArrow);

    framesContainerParent.appendChild(framesContainer);

    secondSection.appendChild(framesContainerParent);

    Ps.initialize(framesContainer);
    elem.appendChild(firstSection);
    elem.appendChild(secondSection);

    framesContainer.addEventListener('click', function (e) {

        e.stopPropagation();

        var mainElem = e.target.parentNode
        if(!mainElem.className.includes('backgroundFrameElem')){
            return
        }

        onOff.checked = true;

        var frames = framesContainer.querySelectorAll('.backgroundFrameElem');

        for (var i = 0; i < frames.length; i++) {

            var frame = frames[i];
            frame.className = 'backgroundFrameElem';

        }

        backgroundFrameID = mainElem.getAttribute('data-id');


        mainElem.className = 'backgroundFrameElem active';

        onOff.checked = true;

        var frames = framesContainer.querySelectorAll('.backgroundFrameElem');

        for (var i = 0; i < frames.length; i++) {

            var frame = frames[i];
            frame.className = 'backgroundFrameElem';

        }

        changeInRange()
    });

    Editor.webSocketControllers.theme.getBackgroundFrames(Editor.adminProject.format.theme.getID(), function (data) {

        function prepareFrameElement(frameData) {

            var elem = document.createElement('div');
            elem.className = frameData._id == backgroundFrameID ? 'backgroundFrameElem active' : 'backgroundFrameElem';
            elem.setAttribute('data-id', frameData._id);

            var img = document.createElement('img');
            img.src = EDITOR_ENV.staticUrl + frameData.ProjectImage.thumbnail;

            var imageHelper = document.createElement('div');
            imageHelper.className = 'backgroundFrame helper';
            imageHelper.style.left = frameData.x + "%";
            imageHelper.style.top = frameData.y + "%";
            imageHelper.style.width = frameData.width + "%";
            imageHelper.style.height = frameData.height + "%";

            elem.appendChild(img);
            elem.appendChild(imageHelper);

            return elem;

        }

        for (var i = 0; i < data.length; i++) {

            framesInner.appendChild(prepareFrameElement(data[i]));

        }

        framesInner.style.width = '100%';

    });

    return elem;

};

p.createShadowTool = function () {

    var _this = this;
    var object = this.proposedPositionInstance;
    var Editor = object.editor;
    var tool = document.createElement('div');
    tool.className = 'button';
    tool.id = 'shadowButton';
    //tool.innerHTML = 'C';

    tool.appendChild(Editor.template.createToolhelper('Dodaj cień do zdjęcia', 'none', 'infoBoxShadow'));

    tool.addEventListener('click', function (e) {

        e.stopPropagation();

        if (_this.openSection == 'shadow' || _this.openSection != null) {

            _this.toolsContainer.removeChild(_this.currentExtendedTool);

            if (_this.openSection != null) {

                _this.toolsContainer.appendChild(_this.initShadowBoxTool());
                _this._updateToolsBoxPosition();

            } else {

                _this.openSection = null;

            }

        } else {

            _this.toolsContainer.appendChild(_this.initShadowBoxTool());
            _this._updateToolsBoxPosition();
        }

    });

    return tool;

    $('#shadowButton').addClass("shadowButton");

    var contextMenuShadowController = document.createElement('div');

    contextMenuShadowController.id = 'contextMenuShadowController';
    contextMenuShadowController.className = 'contextMenuShadowController';
    contextMenuShadowController.addEventListener('click', function (e) {

        e.stopPropagation();

    });

    let menuShadowOpen
    let menuBorderOpen

    tool.addEventListener('click', function (e) {
        e.stopPropagation();
        if (menuShadowOpen == false) {

            if ($('#contextMenuBorderController').hasClass('visibleOn')) {
                $('#contextMenuBorderController').removeClass('visibleOn');
                menuBorderOpen = false;

            }

            if (document.getElementById("infoBoxBorder")) document.getElementById("infoBoxBorder").remove();
            if (document.getElementById("infoBoxShadow")) document.getElementById("infoBoxShadow").remove();

            $(contextMenuShadowController).addClass('visibleOn');
            menuShadowOpen = !menuShadowOpen;
        } else if (menuShadowOpen == true) {
            menuShadowOpen = !menuShadowOpen;
            $(contextMenuShadowController).removeClass('visibleOn');

            var tempTool = document.getElementById('borderButton');

            tempTool.appendChild(Editor.template.createToolhelper("Dodaj ramkę do zdjęcia", 'none', 'infoBoxBorder'));
            tool.appendChild(Editor.template.createToolhelper('Dodaj cień do zdjęcia', 'none', 'infoBoxShadow'));
        }
    });


    var shadowSettings = document.createElement('div');
    shadowSettings.className = 'shadowSettings';

    var shadowSettingsTitle = document.createElement('h4')
    shadowSettingsTitle.className = 'shadowSettingsTitle';
    shadowSettingsTitle.innerHTML = 'Cień';

    shadowSettings.appendChild(shadowSettingsTitle);

    var flipSwitchs2 = generateFlatSwitch(_this.proposedPositionInstance.dropShadow);

    var shadowSwitch = document.createElement('label');
    shadowSwitch.className = 'ShadowSwitchLabel';
    shadowSwitch.innerHTML = (!_this.proposedPositionInstance.dropShadow) ? 'Włącz cień:' : 'Wyłącz cień';

    var _this = this;

    shadowSwitch.addEventListener('change', function (e) {

        //console.log( e );
        e.stopPropagation();
        if (e.target.checked) {


            shadowSwitch.innerHTML = 'Wyłącz cień:';
            shadowSwitch.appendChild(flipSwitchs2);
            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            editingObject.dropShadowAdd();

            Editor.webSocketControllers.editorBitmap.setAttributes(
                editingObject.objectInside.dbID,
                Editor.adminProject.format.view.getId(),
                {

                    dropShadow: true

                }
            );

        } else {

            shadowSwitch.innerHTML = 'Włącz cień:';
            shadowSwitch.appendChild(flipSwitchs2);
            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            editingObject.unDropShadow();

            Editor.webSocketControllers.editorBitmap.setAttributes(
                editingObject.objectInside.dbID,
                Editor.adminProject.format.view.getId(),
                {

                    dropShadow: false

                }
            );

            //console.log('editinfundropShadow' );

        }
    });


    shadowSwitch.appendChild(flipSwitchs2);
    shadowSettings.appendChild(shadowSwitch);


    var shadowMoveXLabel = document.createElement('label');
    shadowMoveXLabel.className = 'shadowToolsClass inputRight';
    shadowMoveXLabel.innerHTML = 'Przesunięcie X:'


    var shadowMoveXInput = document.createElement('input');
    shadowMoveXInput.id = 'shadowMoveXInput';
    shadowMoveXInput.className = 'spinner';
    shadowMoveXInput.value = 1;
    shadowMoveXLabel.appendChild(shadowMoveXInput);

    shadowSettings.appendChild(shadowMoveXLabel);


    var shadowMoveYLabel = document.createElement('label');
    shadowMoveYLabel.className = 'shadowToolsClass inputRight';
    shadowMoveYLabel.innerHTML = 'Przesunięcie Y:';


    var shadowMoveYInput = document.createElement('input');
    shadowMoveYInput.id = 'shadowMoveYInput';
    shadowMoveYInput.className = 'spinner';
    shadowMoveYInput.value = 1;
    shadowMoveYLabel.appendChild(shadowMoveYInput);

    shadowSettings.appendChild(shadowMoveYLabel);

    $(shadowMoveYInput).spinner({
        spin: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            Editor.webSocketControllers.editorBitmap.setAttributes(
                editingObject.objectInside.dbID,
                Editor.adminProject.format.view.getId(),
                {

                    shadowOffsetY: parseInt(event.target.value)

                }
            );
            editingObject.updateShadow();

        },

        change: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowOffsetY(parseInt(event.target.value));

            Editor.webSocketControllers.editorBitmap.setAttributes(
                editingObject.objectInside.dbID,
                Editor.adminProject.format.view.getId(),
                {

                    shadowOffsetY: parseInt(event.target.value)

                }
            );


        },

        stop: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowOffsetY(parseInt(event.target.value));
            //console.log(":::*** editingObject.setShadowOffsetY( parseInt(event.target.value) ) ***:::");

            Editor.webSocketControllers.editorBitmap.setAttributes(
                editingObject.objectInside.dbID,
                Editor.adminProject.format.view.getId(),
                {

                    shadowOffsetY: parseInt(event.target.value)

                }
            );

        }

    }).val(object.shadowOffsetY);


    $(shadowMoveXInput).spinner({
        spin: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowOffsetX(parseInt(event.target.value));

            editingObject.updateShadow();

        },

        change: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowOffsetX(parseInt(event.target.value));

        },

        stop: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowOffsetX(parseInt(event.target.value));

        }

    }).val(object.shadowOffsetX);

    var shadowBlurLabel = document.createElement('label');
    shadowBlurLabel.className = 'shadowToolsClass inputRight';
    shadowBlurLabel.id = 'shadowBlurLabel';
    shadowBlurLabel.innerHTML = 'Rozmycie:';

    var shadowBlurInput = document.createElement('input');
    shadowBlurInput.id = 'shadowBlurInput';
    shadowBlurInput.value = 1;
    shadowBlurInput.className = 'spinner';

    shadowBlurLabel.appendChild(shadowBlurInput);
    shadowSettings.appendChild(shadowBlurLabel);

    $(shadowBlurInput).spinner({
        min: 0,
        value: object.shadowBlur,
        spin: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            editingObject.setShadowBlur(parseInt(event.target.value));
            editingObject.updateShadow();

        },

        change: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            editingObject.setShadowBlur(parseInt(event.target.value));

        },

        stop: function (event) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);
            editingObject.setShadowBlur(parseInt(event.target.value));

        }

    }).val(object.shadowBlur);


    var shadowColorPickerLabel = document.createElement('label');
    shadowColorPickerLabel.className = 'shadowColorPickerLabel'
    //shadowColorPickerLabel.innerHTML = "K:";

    var shadowColor = document.createElement('input');
    shadowColor.id = 'shadowColor';
    shadowColor.className = 'spinner cp-full';

    shadowColorPickerLabel.appendChild(shadowColor);
    shadowSettings.appendChild(shadowColorPickerLabel);

    $(shadowColor).colorpicker({
        parts: 'full',
        showOn: 'both',
        buttonColorize: true,
        showNoneButton: true,
        alpha: true,
        select: function (e) {

            var editing_id = Editor.tools.getEditObject();
            var editingObject = Editor.stage.getObjectById(editing_id);

            var shadowColor = e.target.value;

            var alpha = shadowColor.split('(')[1].split(')')[0].split(',');
            shadowColor = 'rgba(' + alpha[0] + ',' + alpha[1] + ',' + alpha[2] + ',' + (alpha[3] * 255) + ')';

            editingObject.setShadowColor(shadowColor);

            editingObject.updateShadow();

        },

        colorFormat: 'RGBA'

    });

    contextMenuShadowController.appendChild(shadowSettings);

    tool.appendChild(contextMenuShadowController);

    return tool;

};

p.initShadowBoxTool = function () {

    const object = this.proposedPositionInstance;
    const Editor = object.editor;

    function generalizedShadowChange (property, value, singleElem, allElemInPage) {

        let setterName;
        if (property === 'shadowBlur')
            setterName = 'setShadowBlur';
        else if (property === 'shadowColor')
            setterName = 'setShadowColor';
        else if (property === 'shadowOffsetX')
            setterName = 'setShadowOffsetX';
        else if (property === 'shadowOffsetY')
            setterName = 'setShadowOffsetY';

        if ($(singleElem).hasClass('active')) {

            var editingObject = Editor.stage.getObjectById(Editor.tools.getEditObject());
            editingObject[setterName](value);
            editingObject.updateShadow();

        } else if ($(allElemInPage).hasClass('active')) {
            Editor.getEditableObjectsByType(RANGE.allElemInPage, 'ProposedPosition')
                .forEach((eo) => {
                    eo[setterName](value);
                    eo.updateShadow();
                });

        }
        rangeChange(currentRange)
    }

    function setShadowColor(color, save, singleElem, allElemInPage) {
        generalizedShadowChange('shadowColor', color, singleElem, allElemInPage);
    };

    function changeShadowBlur(size, save, singleElem, allElemInPage) {
        generalizedShadowChange('shadowBlur', size, singleElem, allElemInPage);
    }

    function changeOffsetX(size, save, singleElem, allElemInPage) {
        generalizedShadowChange('shadowOffsetX', size, singleElem, allElemInPage);
    }

    function changeOffsetY(size, save, singleElem, allElemInPage) {
        generalizedShadowChange('shadowOffsetY', size, singleElem, allElemInPage);

    }

    function changeDropSettings(value, save, singleElem, allElemInPage) {

        if ($(singleElem).hasClass('active')) {

            if (value) {

                const editingObject = Editor.stage.getObjectById(Editor.tools.getEditObject());
                editingObject.dropShadow=value
                editingObject.dropShadowAdd();


            } else {

                const editingObject = Editor.stage.getObjectById(Editor.tools.getEditObject());
                editingObject.dropShadow=value
                editingObject.unDropShadow();


            }

        } else if ($(allElemInPage).hasClass('active')) {

            Editor.getEditableObjectsByType(RANGE.allElemInPage, 'ProposedPosition')
                .forEach((eo) => {
                    eo.dropShadow=value
                    if (value) {
                        eo.dropShadowAdd();
                    } else {
                        eo.unDropShadow();
                    }
                });

        }
        rangeChange(currentRange)
    };
    let currentRange = RANGE.singleElem

    function rangeChange(range) {
        if (range == RANGE.allElemInPage) {
            const editingObject = Editor.stage.getObjectById(Editor.tools.getEditObject());
            Editor.getEditableObjectsByType(range, 'ProposedPosition')
                .forEach((eo) => {
                    if (editingObject.dropShadow) {
                        eo.dropShadowAdd();
                    } else {
                        eo.unDropShadow();
                    }
                    eo.dropShadow = editingObject.dropShadow
                    eo.setShadowBlur(editingObject.shadowBlur)
                    eo.setShadowColor(editingObject.shadowColor)
                    eo.setShadowOffsetX(editingObject.shadowOffsetX)
                    eo.setShadowOffsetY(editingObject.shadowOffsetY)
                    eo.updateShadow()
                });
        }
        currentRange = range
    }

    return ContextMenuTools.initShadowBoxTool(this,changeDropSettings,  setShadowColor, changeShadowBlur, changeOffsetX, changeOffsetY, [], rangeChange);
};

p.removeImageTool = function () {

    var proposedPositionInstance = this.proposedPositionInstance;
    var tool = document.createElement('div');
    tool.className = 'button';
    tool.id = 'removeImage';
    tool.addEventListener('click', (e) => {
        e.stopPropagation();
        proposedPositionInstance.parent.removeChild(proposedPositionInstance)
        Editor.tools.setEditingObject(null);
        Editor.tools.init();
        $("#proposedTemplate-toolsbox").remove();
    })
    return tool;

};


/**
 * Aktualizuje pozycję elementu z narzędziami
 *
 * @method _updateToolsBoxPosition
 */
p._updateToolsBoxPosition = function () {

    var tools = this.toolsContainer;
    var object = this.proposedPositionInstance;
    var Editor = object.editor;

    if (this.useType == "admin")
        var adminTools = $('#proposed-position-tool-admin');

    var toolSize = {

        width: $(tools).innerWidth(),
        height: $(tools).innerHeight()

    };

    var pos = this.proposedPositionInstance.getGlobalPosition();
    var stage = Editor.getStage();
    var bounds = this.proposedPositionInstance.getTransformedBounds();

    $(tools).css({top: pos[1] + (bounds.height / 2) * stage.scaleY + 100, left: pos[0] - toolSize.width / 2});

    var size = parseInt($(tools).css('top')) + $(tools).height();

    var top = parseInt($(tools).css('top'));

    if (size > window.innerHeight) {

        var diff = size - window.innerHeight;
        $(tools).css('top', top - diff - 10);

    }

};

export {ProposedPositionContextMenu};
