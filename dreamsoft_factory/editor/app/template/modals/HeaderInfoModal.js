import React from 'react'
import ImagesButtonsList from "../toolsBox/buttons/ImagesButtonsList";
import ProposedTemplatesButtonsList from "../toolsBox/buttons/ProposedTemplatesButtonsList";
import ThemesButtonsList from "../toolsBox/buttons/ThemesButtonsList";
import ClipartsButtonsList from '../toolsBox/buttons/ClipartsButtonsList';
import AttributesButtonsList from '../toolsBox/buttons/AttributesButtonsList';
import LayersButtonsList from '../toolsBox/buttons/LayersButtonsList';
import PositionsButtonsList from '../toolsBox/buttons/PositionsButtonsList';
import ModalContent from "./components/ModalContent";
import ModalHeader from "./components/ModalHeader";
import ModalBody from "./components/ModalBody";

const HeaderInfoModal = () => {
    const toolsButtons = [ImagesButtonsList, ProposedTemplatesButtonsList, ThemesButtonsList, ClipartsButtonsList, AttributesButtonsList, LayersButtonsList, PositionsButtonsList]

    return (
        <ModalContent id={"infoModal"} className={'modal-xl'}>
            <ModalHeader title={"Znaczenie ikon i opisy funkcji"}>
                <div className={'modal-icon'}>i</div>
            </ModalHeader>
            <ModalBody>
                <div className={'modal-nav-header-container'}>
                    {toolsButtons.map((tool, index) => (
                        <div className={'modal-info-section'} key={index}>
                            <div className={'modal-navigation-tool-button-container'}>
                                <tool.Component usedInModal/>
                                <span>
                                    {tool.description}
                                </span>
                            </div>
                            <div className={'modal-tool-inner-buttons-container'}>
                                {Object.values(tool.Components).map((button, buttonIndex) => {
                                        // has nested buttons
                                        return button.hasOwnProperty('buttons') ? button.buttons.map((innerButton, innerButtonIndex) =>
                                            (<div className={"modal-tool-single-button-container"}
                                                  key={innerButtonIndex}>
                                                <div className={"modal-button-container"}>
                                                    <innerButton.Component usedInModal/>
                                                </div>
                                                <span>{innerButton.description}</span>
                                            </div>)
                                        ) : (
                                            <div className={"modal-tool-single-button-container"}
                                                 key={buttonIndex}>
                                                <div className={"modal-button-container"}>
                                                    <button.Component usedInModal/>
                                                </div>
                                                <span>{button.description}</span>
                                            </div>
                                        )
                                    }
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </ModalBody>
        </ModalContent>
    )
}

export default HeaderInfoModal