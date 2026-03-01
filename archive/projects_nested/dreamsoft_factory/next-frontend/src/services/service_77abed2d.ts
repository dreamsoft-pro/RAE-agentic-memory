import api from "@/lib/api";

class MyClass {
    private _uiHash: () => any;
    private _trigger: (event: string, e?: Event, ui?: any) => boolean | void;
    private cancel: () => void;

    constructor() {
        this._uiHash = this._uiHash.bind(this);
        this._trigger = this._trigger.bind(this);
        this.cancel = this.cancel.bind(this);
    }

    public myMethod(event: Event, noPropagation?: boolean): boolean {
        if (!noPropagation) {
            this._trigger("beforeStop", event, this._uiHash());
        }

        this.placeholder[0].parentNode.removeChild(this.placeholder[0]);

        if (!this.cancelHelperRemoval) {
            if (this.helper[0] !== this.currentItem[0]) {
                this.helper.remove();
            }
            this.helper = null;
        }

        if (!noPropagation) {
            for (let i = 0; i < delayedTriggers.length; i++) {
                delayedTriggers[i].call(this, event);
            }
            this._trigger("stop", event, this._uiHash());
        }

        this.fromOutside = false;
        return !this.cancelHelperRemoval;
    }

    private _trigger(event: string, e?: Event, ui?: any): boolean | void {
        if ($.Widget.prototype._trigger.apply(this, arguments) === false) {
            this.cancel();
        }
    }
}