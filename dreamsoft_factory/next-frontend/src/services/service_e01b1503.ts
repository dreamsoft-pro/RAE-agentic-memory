import api from '@/lib/api';
import { NextApiRequest, NextApiResponse } from 'next';

class CookieManager {
    setCookie(name: string, value: string, domainName: string, expirationDate: Date) {
        document.cookie = `${name}=${value}; domain=${domainName}; path=/; expires=${expirationDate.toUTCString()}`;
    }
}

class TemplateIncluder {
    includeTemplateVariables(scope: any, templateName: string, groupID?: number, typeID?: number, categoryID?: number, all?: boolean) {
        // Assuming this function needs to perform some async operation using 'api' module
        return api.get(`someEndpoint?template=${templateName}${groupID ? `&groupId=${groupID}` : ''}${typeID ? `&typeId=${typeID}` : ''}${categoryID ? `&categoryId=${categoryID}` : ''}${all ? `&all=${all}` : ''}`)
            .then(response => {
                // Handle the response
                return response.data;
            })
            .catch(error => {
                console.error('Error fetching template variables:', error);
                throw new Error('Failed to include template variables');
            });
    }
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const cookieManager = new CookieManager();
    const templateIncluder = new TemplateIncluder();

    // Example usage
    const expirationDate = new Date(new Date().getTime() + 30 * 24 * 60 * 60 * 1000); // 30 days from now

    cookieManager.setCookie('user', 'John Doe', '.example.com', expirationDate);

    templateIncluder.includeTemplateVariables({}, 'home-template')
        .then(data => res.json({ message: 'Template variables included successfully', data }))
        .catch(error => res.status(500).json({ error }));
}