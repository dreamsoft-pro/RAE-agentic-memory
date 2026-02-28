import React from 'react';
import ChangeColumnsButtons from "../content/ChangeColumnsButtons";
import ToolButton from "../navigation/ToolButton";
import MainButton from "../content/advanced/cliparts/MainButton";
import CategorySelector from "../content/advanced/cliparts/CategorySelector";

const ClipartsButtonsList = {
    Component: ({...props}) => <ToolButton className={"cliparts"} {...props} />,
    title: "Cliparty",
    description: "W tym narzędziu możesz dodać cliparty.",
    Components: {
        MainButton: {
            Component: ({...props}) => <MainButton {...props} />,
            description: "Sekcja układ zdjęć"
        },
        ChangeColumns: {
            Component: ({...props}) => <ChangeColumnsButtons option={"cliparts"} {...props} />,
            description: "Zmień ilość kolumn wyświetlania clipartów"
        },
        CategorySelector: {
            // this buttons need to be rebuilt into shared component (design is the same in cliparts, attributes and proposedTemplates tools)
            Component: ({...props}) => <CategorySelector {...props} />,
            description: "Wybierz interesującą Cię kategorię",
        }
    }
}

export default ClipartsButtonsList;