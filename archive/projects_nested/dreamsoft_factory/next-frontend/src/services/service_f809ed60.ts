import api from "@/lib/api";

class MyComponent extends React.Component {
    private calculatePages = async (type: any, value: number): Promise<number> => {
        let sheets: number;
        let pages: number;

        sheets = type.thickness.min / value;
        pages = Math.ceil(sheets) * 2;
        
        const doublePage = !!type.pages[0]?.doublePage;
        if (doublePage) {
            pages *= 2;
        }

        const step = type.pages[0]?.step;
        if (typeof step !== 'undefined') {
            const modulo: number = pages % step;
            if (modulo > 0) {
                pages += step - modulo;
            }
        }

        if (type.currentPages < pages) {
            // show that pages was change
            this.selectPages(type, pages);
        }

        return pages;
    };

    private selectPages = (type: any, newPages: number): void => {
        // Your logic for selecting pages goes here
    };
}