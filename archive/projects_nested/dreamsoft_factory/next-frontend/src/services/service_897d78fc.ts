import api from '@/lib/api';

export default class UtilityService {
    private resource: string;
    private url: string;

    constructor(resource: string = 'defaultResource', url: string = 'https://api.example.com') {
        this.resource = resource;
        this.url = url;
    }

    public async getMegaMenu(): Promise<any> {
        const response = await api.get(`${this.url}/mega-menu/${this.resource}`);
        return response.data;
    }

    public async getSkinName(): Promise<string> {
        const response = await api.get(`${this.url}/skin-name/${this.resource}`);
        return response.data.name;
    }

    public async getForms(): Promise<any[]> {
        const response = await api.get(`${this.url}/forms/${this.resource}`);
        return response.data.forms;
    }

    public formatSizeUnits(bytes: number): string {
        if (bytes === 0) return '0 B';
        const k = 1024,
            dm = 3,
            sizes = ['B', 'KB', 'MB', 'GB', 'TB'],
            i = Math.min((bytes === 0 ? 0 : parseInt(Math.floor(Math.log(bytes) / Math.log(k)), 10)), dm);
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    public handleGoTop(): void {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    public async getCreditLimitInfo(): Promise<any> {
        const response = await api.get(`${this.url}/credit-limit-info/${this.resource}`);
        return response.data;
    }

    public getCookie(name: string): string | null {
        const nameEQ = name + '=';
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    public setCookie(name: string, value: string, daysToExpire?: number): void {
        const date = new Date();
        if (daysToExpire) {
            date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
        }
        document.cookie = `${name}=${value};expires=${date.toUTCString()}`;
    }

    public includeTemplateVariables(template: string, variables: { [key: string]: any }): string {
        return Object.entries(variables).reduce((acc, [key, value]) => acc.replace(`{{${key}}}`, value), template);
    }

    public getTemplateVariable(name: string): string | null {
        const regex = new RegExp(`\\{\\{(${name})\\}\\}`);
        return (document.body.innerHTML.match(regex) || [''])[1];
    }
}