import api from "@/lib/api";

class ModuleValueService {
    private module: string;
    private resource: string;

    constructor(module: string) {
        this.module = module;
        this.resource = ['modules', this.module, 'module_values'].join('/');
        this.getAllDef = null; // Ensure variable is defined before use
    }

    private getAllDef: Promise<any> | null;

    public async getAll(force?: boolean): Promise<void> {
        if (this.getAllDef === null || force) {
            this.getAllDef = api.get(this.resource).then((response) => {
                console.log('Data retrieved:', response.data);
                // Handle data here, e.g., update state or store in cache
                return;
            }).catch((error) => {
                console.error("Error fetching module values:", error);
            });
        }

        await this.getAllDef; // Wait for the promise to resolve/reject
    }
}

export default ModuleValueService;