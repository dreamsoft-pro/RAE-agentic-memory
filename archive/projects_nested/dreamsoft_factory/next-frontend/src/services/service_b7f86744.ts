import api from "@/lib/api";
import _ from "lodash";

export default class ProductManager {
    private editorUrl: string;
    private returnedProduct: any; // Assuming this is an object structure similar to what you've described.
    private $scope: { [key: string]: any };
    private realisationTimes: Array<{ ID: number, overwriteDate?: Date }>;
    private rememberVolume: { realisationTime?: any };

    constructor() {
        this.editorUrl = "";
        this.returnedProduct = {}; // Initialize as per your data structure.
        this.$scope = {};
        this.realisationTimes = [];
        this.rememberVolume = {};
    }

    processOptions(): void {
        _.each(this.returnedProduct.options, (opt) => {
            this.editorUrl += `&${opt.attrID}=${opt.optID}`;
        });
    }

    checkVolume(realisationTime: { ID: number; date?: Date }): void {
        _.each(this.$scope.realisationTimes, (val) => {
            val.overwriteDate = null;
        });

        const idxRT = _.findIndex(this.$scope.realisationTimes, { ID: realisationTime.ID });
        if (idxRT !== -1) {
            this.rememberVolume.realisationTime = this.$scope.realisationTimes[idxRT];
            this.$scope.realisationTimes[idxRT].overwriteDate = realisationTime.date;
        }
    }

    async fetchData(url: string): Promise<void> {
        try {
            const response = await api.get(url);
            // Assuming returnedProduct is one of the things you get back from your API.
            this.returnedProduct = response.data.returnedProduct;
            this.processOptions();
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    async updateRealisationDates(): Promise<void> {
        try {
            for (const rt of this.$scope.realisationTimes) {
                await api.put(`/update/realisation/${rt.ID}`, { overwriteDate: rt.overwriteDate });
            }
        } catch (error) {
            console.error("Error updating realisation dates:", error);
        }
    }
}