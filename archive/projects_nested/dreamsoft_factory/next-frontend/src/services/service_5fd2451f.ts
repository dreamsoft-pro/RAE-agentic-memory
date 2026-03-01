import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class TextWidgetService {
    private data: any;

    constructor(data: any) {
        Object.assign(this, data);
    }

    findWord = (html: string, lines: number): string | false => {
        const plainText = new DOMParser().parseFromString(html, "text/html").documentElement.textContent;
        const splitText = plainText.split(' ');
        let chars = 0;

        for(let i = 0; i < splitText.length; i++) {
            chars += splitText[i].length;
            if(chars >= lines) {
                return splitText[i];
            }
        }

        return false;
    };

    findParagraph = (html: string, word: string): HTMLElement[] => {
        const paragraphs = new DOMParser().parseFromString(html, "text/html").querySelectorAll('p');
        // Further processing to find paragraph containing the specific word
        return Array.from(paragraphs);
    };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    try {
        const textWidgetService = new TextWidgetService({ /* initialize with necessary data */ });
        const html = req.query.html as string;
        const lines = parseInt(req.query.lines as string);

        const word = textWidgetService.findWord(html, lines);
        const paragraphs = textWidgetService.findParagraph(html, word);

        res.status(200).json({ word: word, paragraphs: Array.from(paragraphs) });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal server error' });
    }
}