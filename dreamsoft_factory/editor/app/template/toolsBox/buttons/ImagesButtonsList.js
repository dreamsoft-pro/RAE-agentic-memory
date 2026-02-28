import React from 'react';
import ChangeColumnsButtons from "../content/ChangeColumnsButtons";
import FillImagesAutomaticallyButton from "../content/simple/images/FillImagesAutomaticallyButton";
import UsedNotUsedImagesSwapper from "../content/simple/images/UsedNotUsedImagesSwapper";
import ShowAllPhotosButton from "../content/simple/images/ShowAllPhotosButton";
import ShowNotUsedPhotosButton from "../content/simple/images/ShotNotUsedPhotosButton";
import ReorderImagesButton from "../content/simple/images/ReorderImagesButton";
import ToolButton from "../navigation/ToolButton";
import UploadButton from "../content/simple/images/UploadButton";

// Objekt stworzony w celu dynamicznego generowania kontentu w modal'u, który odpowiedzialny jest za informacje dotyczące obłsugi edytora
// Zawiera listę przycisków, które są potrzebne do wygenerowania narzędzia do zdjęć

//Gdy zmienim narzędzie w toolboxie, usuwana jest klasa active, zrobić usuwanie wyłącznie dla toolxbox'a!
const ImagesButtonsList = {
    Component: ({...props}) => <ToolButton className={"images"} {...props} />,
    title: "Zdjęcia",
    description: "Menu zdjęć, dodaj zdjęcie, zmień kolejność, pokaż użyte zdjęcia",
    Components: {
        Upload: {
            Component: ({...props}) => <UploadButton  {...props} />,
            description: "Dodaj zdjęcia ze swojego urządzenia"
        },
        ChangeColumns: {
            Component: ({...props}) => <ChangeColumnsButtons option={"images"} {...props} />,
            description: "Zmień ilość kolumn wyświetlania zdjęć"
        },
        FillImagesAutomatically: {
            Component: ({...props}) => <FillImagesAutomaticallyButton  {...props} />,
            description: "Automatycznie dodaj zdjęcia ze wględu na ich aktualną kolejność, po sortowaniu ustawi zdjęcia w nowej kolejności"
        },
        UsedNotUsedImagesSwapper: {
            Component: ({...props}) => <UsedNotUsedImagesSwapper {...props} />,
            // ten komponent zawiera przyciski, które podmieniają się po kliknięciu, obejście dodatkową listą
            buttons: [
                {
                    Component: ({...props}) => <ShowAllPhotosButton  {...props} />,
                    description: "Pokaż wszystkie zdjęcia znajdujące się w obecnym projekcje"
                },
                {
                    Component: ({...props}) => <ShowNotUsedPhotosButton  {...props} />,
                    description: "Pokaż wszystkie zdjęcia, które nie zostały jeszcze użyte"
                },
            ]
        },
        ReorderImages: {
            Component: ({...props}) => <ReorderImagesButton  {...props} />,
            description: "Wyświetl menu, w którym zmienisz kolejność dodanych zdjęć"
        },
    }
}

export default ImagesButtonsList;