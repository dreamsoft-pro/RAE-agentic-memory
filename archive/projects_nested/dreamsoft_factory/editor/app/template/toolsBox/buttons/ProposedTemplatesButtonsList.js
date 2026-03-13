import React from 'react';
import ToolButton from "../navigation/ToolButton";
import AllLayoutsButton from "../content/simple/proposedTemplates/AllLayoutsButton";
import MainButton from "../content/simple/proposedTemplates/MainButton";
import ProposedPositionGroup from "../content/simple/proposedTemplates/ProposedPositionGroup";
import ChangeColumnsButtons from "../content/ChangeColumnsButtons";

const ProposedTemplatesButtonsList = {
    Component: ({...props}) => <ToolButton className={"templates"} {...props} />,
    title: "Układy zdjęć",
    description: "Układy zdjęć i tekstów",
    Components: {
        MainButton: {
            Component: ({...props}) => <MainButton {...props} />,
            description: "Sekcja układ zdjęć"
        },
        ChangeColumns: {
            Component: ({...props}) => <ChangeColumnsButtons option={"templates"} {...props} />,
            description: "Zmień ilość kolumn wyświetlania układów"
        },
        AllLayouts: {
            Component: ({...props}) => <AllLayoutsButton {...props} />,
            description: "Rozwiń wszystkie układy zdjęć oraz tekstów"
        },
        // ProposedPositionGroup: {
        //     Component: ({...props}) => <ProposedPositionGroup {...props} />,
        //     description: "Rozwiń wybraną sekcję układów"
        // }
    }
}

export default ProposedTemplatesButtonsList;