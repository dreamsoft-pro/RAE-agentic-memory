import React from 'react';
import ToolButton from "../navigation/ToolButton";
import MainButton from "../content/advanced/layers/MainButton";
import Padlock from "../content/advanced/layers/Padlock";
import Brush from "../content/advanced/layers/Brush";
import Visibility from "../content/advanced/layers/Visibility";

const LayersButtonsList = {
    Component: ({ ...props }) => <ToolButton className={"layers"} {...props} />,
    title: "Warstwy",
    description: "W tym narzędziu możesz zarządzać warstwami.",
    Components: {
        MainButton: {
            Component: ({ ...props }) => <MainButton {...props} />,
            description: "Sekcja zarządzania warstwami",
        },
        Padlock: {
            Component: ({ ...props }) => <Padlock {...props} />,
            description: "Zablokuj/odblokuj warstwę",
        },
        Brush: {
            Component: ({ ...props }) => <Brush {...props} />,
            description: "Zmień styl pędzla dla warstwy",
        },
        Visibility: {
            Component: ({ ...props }) => <Visibility {...props} />,
            description: "Pokaż/ukryj warstwę",
        },
    },
};

export default LayersButtonsList;
