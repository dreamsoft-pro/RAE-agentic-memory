import api from "@/lib/api";

class Menu {
    private version: string;
    private defaultElement: string;
    private delay: number;
    private options: Record<string, any>;
    private activeMenu: HTMLElement;

    constructor() {
        this.version = "1.11.4";
        this.defaultElement = "<ul>";
        this.delay = 300;
        this.options = {
            icons: { submenu: "ui-icon-carat-1-e" },
            items: "> *",
            menus: "ul",
            position: { my: "left-1 top", at: "right top" },
            role: "menu",
            blur: null,
            focus: null,
            select: null
        };
    }

    private _create(): void {
        this.activeMenu = document.createElement(this.defaultElement);
    }
}

// Example of using the Menu class (hypothetical interaction)
const menuInstance = new Menu();
menuInstance._create();

// If you wanted to simulate fetching data or making API calls:
async function fetchMenuData() {
    try {
        const response = await api.get('some-endpoint');
        console.log(response.data);
    } catch (error) {
        console.error("Failed to fetch menu data", error);
    }
}