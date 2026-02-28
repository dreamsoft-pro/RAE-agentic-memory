import React, {useEffect, useState} from 'react';
import ProposedTemplatesButtonsList from "../../../buttons/ProposedTemplatesButtonsList";
import {useSelector} from "react-redux";
import ProposedPositionGroup from "./ProposedPositionGroup";
import Switch from "../../../../../components/Switch";
import {store} from "../../../../../ReactSetup";
import {
    setExpandedSelectors,
    updateTemplatesShowingType
} from "../../../../../redux/reducers/templates/templates";

const ProposedTemplatesToolContent = ({editor, className = ""}) => {
    const {data, allTemplates, expandedSelectors} = useSelector(state => state.templatesReducer);

    console.log(allTemplates)

    const [templates, setTemplates] = useState({});
    const [allLayoutsExpanded, setAllLayoutsExpanded] = useState(false);
    // array of each group showing flag

    // grouping proposedTemplates by images count
    const groupTemplatesBy = (data, property) => {
        const grouped = data.reduce((acc, template) => {
            const key = template[property] || 'undefined'; // Group by specified property or 'undefined'
            if (!acc[key]) {
                acc[key] = [];
            }
            acc[key].push(template);
            return acc;
        }, {});

        return Object.values(grouped);
    }

    // adding switching on / off in future admin panel
    const showLocalTemplatesSwitch = true;

    // Function to toggle all layouts
    const toggleAllLayouts = () => {
        setAllLayoutsExpanded(prevLayouts => {
            store.dispatch(setExpandedSelectors(expandedSelectors.map(selector => ({
                ...selector,
                open: !prevLayouts
            }))));

            return !prevLayouts;
        });
    };

    useEffect(() => {
        const grouped = groupTemplatesBy(data, 'imagesCount')

        // for displaying proposedTemplates
        setTemplates(
            {
                local: grouped.map((group) => group.filter((template) => template.isGlobal)).filter(group => group.length),
                all: grouped
            }
        )

        // when user changes pages, we need to preserve open selectors, which were previously opened
        store.dispatch(setExpandedSelectors(grouped.map(newGroup => {
            const existingState = expandedSelectors.find(group => group.imagesCount === newGroup[0].imagesCount);

            const currentSelectedViewGroup = Object.entries(newGroup).some(([_, template]) => {
                return template._id === editor.userProject.getCurrentView().Pages[0]?.ProposedTemplateFrom
            })

            return {
                imagesCount: newGroup[0].imagesCount,
                open: existingState ? existingState.open : currentSelectedViewGroup
            }
        })));

    }, [data]);

    // Inner container for proposedTemplates
    const TemplatesInnerContainer = () => {
        return (
            <div id={"proposedTemplate-content"} className={`templates-inner-container ${className}`}>
                {
                    Object.values(templates).length ?
                        (<div className="proposedTemplateContainer">
                            <div className="buttons-wrapper">
                                <div className="buttons-container">
                                    <ProposedTemplatesButtonsList.Components.MainButton.Component/>
                                    <ProposedTemplatesButtonsList.Components.ChangeColumns.Component
                                        option={"templates"}
                                        element={templates.all.map((group, index) => (`#group-list-${index}`))}/>
                                </div>
                                {showLocalTemplatesSwitch &&
                                    <Switch
                                        id={"switchGlobalLocalTemplates"}
                                        label={{
                                            close: "Układy lokalne",
                                            open: "Wszystkie układy"
                                        }}
                                        checked={allTemplates}
                                        onChange={() => store.dispatch(updateTemplatesShowingType())}
                                    />
                                }

                                <div className={'buttons-container'}>
                                    <ProposedTemplatesButtonsList.Components.AllLayouts.Component
                                        toggleAllLayouts={() => toggleAllLayouts()}
                                        isActive={allLayoutsExpanded}
                                    />
                                </div>
                            </div>
                            {allTemplates ?
                                templates.all.length ? templates.all.map((group, index) => (
                                    <ProposedPositionGroup
                                        key={index}
                                        editor={editor}
                                        group={group}
                                        index={index}
                                    />
                                )) : (<div className={'templates-loading-info'}>Brak danych</div>)
                                : templates.local.length ? templates.local.map((group, index) => (
                                    <ProposedPositionGroup
                                        key={index}
                                        editor={editor}
                                        group={group}
                                        index={index}
                                    />
                                )) : (<div className={'templates-loading-info'}>Brak danych</div>)
                            }
                        </div>)
                        :
                        <div className={'templates-loading-info'}>Wczytuję układy zdjęć...</div>
                }
            </div>
        );
    };

    return TemplatesInnerContainer();
};


export default ProposedTemplatesToolContent;
