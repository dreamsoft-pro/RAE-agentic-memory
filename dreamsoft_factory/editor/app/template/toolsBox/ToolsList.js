import ImagesToolContent from "./content/simple/images/ImagesToolContent";
import ThemesToolContent from "./content/simple/themes/ThemesToolContent";
import AttributesToolContent from "./content/advanced/attributes/AttributesToolContent";
import ProposedTemplatesToolContent from "./content/simple/proposedTemplates/ProposedTemplatesToolContent";
import LayersToolContent from "./content/advanced/layers/LayersToolContent"
import ClipartsToolContent from "./content/advanced/cliparts/ClipartsToolContent";
import PositionsToolContent from "./content/advanced/positions/PositionsToolContent"

// All components used in toolsBox menu
const ToolsList = [
    {
        toolContent: ImagesToolContent,
        toolButton: {
            className: "images",
            text: "Tutaj możesz dodać swoje zdjęcia"
        },
        type: "simple"
    }, {
        toolContent: ThemesToolContent,
        toolButton: {
            className: "themes",
            text: "Tutaj możesz wybrać motyw"
        },
        type: "simple"

    }, {
        toolContent: ProposedTemplatesToolContent,
        toolButton: {
            className: "templates",
            text: "Tutaj możesz zmienić układ zdjęć"
        },
        type: "simple"
    }, {
        toolContent: AttributesToolContent,
        toolButton: {
            className: "attributes",
            text: "Tutaj możesz edytować atrybuty"
        },
        type: "advanced"
    },
    {
        toolContent: LayersToolContent,
        toolButton: {
            className: "layers",
            text: "Tutaj możesz wybrać warstwy"
        },
        type: "advanced"
    },
    // {
    //     toolContent: ClipartsToolContent,
    //     toolButton: {
    //         className: "cliparts",
    //         text: "Tutaj możesz wybrać clipart'y"
    //     },
    //     type: "advanced"
    // },
    {
        toolContent: PositionsToolContent,
        toolButton: {
            className: "positions",
            text: "Tutaj możesz pozycjonować elementy"
        },
        type: "advanced"
    }
];

export default ToolsList