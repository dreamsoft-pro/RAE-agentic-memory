import React from 'react';
import { AngleButton } from '../content/advanced/positions/buttons/AngleButton';
import { BlockButton } from '../content/advanced/positions/buttons/BlockButton';
import { ConnectButton } from '../content/advanced/positions/buttons/ConnectButton';
import { HorizontalReflectButton } from '../content/advanced/positions/buttons/HorizontalReflectButton';
import { VerticalReflectButton } from '../content/advanced/positions/buttons/VerticalReflectButton';
import MainButton from '../content/advanced/positions/buttons/MainButton';
import { LayerUpButton } from '../content/advanced/positions/buttons/LayerUpButton';
import { LayerDownButton } from '../content/advanced/positions/buttons/LayerDownButton';
import ToolButton from '../navigation/ToolButton';

const PositionsButtonsList = {
    Component: ({...props}) => <ToolButton className={"positions"} {...props} />,
    title: "Pozycjonowanie i Wymiary",
    description: "W tym narzędziu możesz edytować wymiary oraz pozycje elementów.",
    Components: {
        MainButton: {
            Component: ({...props}) => <MainButton {...props} />,
            description: "Sekcja pozycjonowania i wymiarów"
        },
        ConnectButton: {
            Component: ({...props}) => <ConnectButton {...props} />,
            description: "Połącz i skaluj wymiary ze sobą"
        },
        AngleButton: {
            Component: ({...props}) => <AngleButton {...props} />,
            description: "Zmień kąt położenia warstwy"
        },
        BlockButton: {
            Component: ({...props}) => <BlockButton {...props} />,
            description: "Zablokuj elementy w danym stanie"
        },
        HorizontalReflectButton: {
            Component: ({...props}) => <HorizontalReflectButton {...props} />,
            description: "Odbicie w poziomie"
        },
        VerticalReflectButton: {
            Component: ({...props}) => <VerticalReflectButton {...props} />,
            description: "Odbicie w pionowie"
        },
        LayerUpButton: {
            Component: ({...props}) => <LayerUpButton {...props} />,
            description: "Przesuń warstwę do góry"
        },
        LayerDownButton: {
            Component: ({...props}) => <LayerDownButton {...props} />,
            description: "Przesuń warstwę w dół"
        }
    }
}

export default PositionsButtonsList;
