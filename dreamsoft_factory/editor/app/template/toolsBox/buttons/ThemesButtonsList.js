import React from 'react';
import AddThemesButton from "../content/simple/themes/AddThemesButton";
import CopyFromThemeButton from "../content/simple/themes/CopyFromThemeButton";
import MainButtonThemes from "../content/simple/themes/MainButtonThemes";
import ToolButton from "../navigation/ToolButton";

const ThemesButtonsList = {
    Component: ({...props}) => <ToolButton className={"themes"} {...props} />,
    title: "Tła",
    description: "Obsługa dodawania, usuwania teł dla poszczególnych stron projektu",
    Components: {
        MainButton: {
            Component: ({...props}) => <MainButtonThemes {...props} />,
            description: "Sekcja wyboru teł"
        },
        AddThemes: {
            Component: ({...props}) => <AddThemesButton {...props}/>,
            description: "Zmień tło indiwidualnie"
        },
        CopyFromTheme: {
            Component: ({...props}) => <CopyFromThemeButton {...props} />,
            description: "Zmień wszystkie tła"
        }
    }
}

export default ThemesButtonsList;