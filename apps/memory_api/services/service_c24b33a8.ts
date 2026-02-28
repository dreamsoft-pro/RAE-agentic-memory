import axios from 'axios';
import { DOMParser } from 'dom-parser';

class DocumentProcessor {
    async processDocument(html: string, word: string): Promise<number | false> {
        const paragraphs = new DOMParser().parseFromString(html, "text/html").querySelectorAll('p');

        if (paragraphs.length === 1) {
            return false;
        }

        for (let i = 0; i < paragraphs.length; i++) {
            const nextElementSiblingText = paragraphs[i].nextElementSibling?.innerHTML.replace(/<[^>]*>/g, "");
            if (nextElementSiblingText && nextElementSiblingText.indexOf(word) !== -1) {
                return i;
            }
        }

        if (typeof word === 'string' && word.length > 0) {
            return 0;
        }
        return false;
    }

    async getLess(html: string, paragraphIndex: number): Promise<string> {
        const paragraphs = new DOMParser().parseFromString(html, "text/html").querySelectorAll('p');

        let template = '';

        for (let i = 0; i < paragraphs.length; i++) {
            template += paragraphs[i].innerHTML;

            if (i === paragraphIndex) {
                return template;
            }
        }

        return '';
    }
}

// Example usage
const documentProcessor = new DocumentProcessor();

documentProcessor.processDocument('<html><body><p>First</p><p>Second</p></body></html>', 'word')
    .then(result => console.log('Result:', result));

documentProcessor.getLess('<html><body><p>First</p><p>Second</p></body></html>', 1)
    .then(result => console.log('Template:', result));