import api from "@/lib/api";

class TooltipManager {
    private _open(event: Event, target: HTMLElement, content: string | Function): void {
        // Assume _open is a method that handles opening the tooltip with provided event/target/content.
        console.log("Opening tooltip with:", event, target, content);
    }

    private _delay(fn: () => void): Promise<void> {
        return new Promise((resolve) => setTimeout(() => resolve(fn()), 100));
    }

    public async showTooltip(event: Event, target: HTMLElement, contentOption: string | ((response: any) => void)): Promise<void> {
        let content = '';

        if (typeof contentOption === "string") {
            return this._open(event, target, contentOption);
        }

        try {
            // Simulate an async call to get the response from some API or function
            const response = await api.get('some-endpoint'); // Replace with actual API call

            content = contentOption.call(target[0], (response: any) => {
                this._delay(() => { // Delay execution of _open method
                    if (!target.data("ui-tooltip-open")) return;

                    event.type = "focusin"; // Assuming a jQuery-like environment but setting the type back for consistency

                    this._open(event, target, response);
                });
            });

            if (content) {
                this._open(event, target, content); // Ensure to call _open with content
            }
        } catch (error) {
            console.error("Failed to fetch content:", error);
        }
    }
}