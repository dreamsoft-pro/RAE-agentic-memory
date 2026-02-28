import { useRouter } from 'next/router';
import api from '@/lib/api'; // Assuming this is correctly implemented elsewhere

class MyComponent extends React.Component {
    constructor(props: any) {
        super(props);
        this.state = {
            currentLang: {},
            attributes: [],
        };
    }

    componentDidMount() {
        const { locale } = useRouter();
        if (locale) {
            this.setState({ currentLang: { code: locale } });
        }
        // Fetch the attributes data
        this.fetchAttributesData();
    }

    async fetchAttributesData() {
        try {
            const response = await api.get('/your-endpoint-here');
            const attributes = response.data;
            this.setState({ attributes });
        } catch (error) {
            console.error("Failed to fetch attributes:", error);
        }
    }

    getAttributeName(attribute: any): string {
        if (!this.state.currentLang.code || !attribute.names || !attribute.attrName) return '';

        let attrName = '';
        
        if (attribute.names[this.state.currentLang.code]?.name !== undefined) {
            attrName = attribute.names[this.state.currentLang.code].name;
        } else {
            attrName = attribute.attrName;
        }

        return attrName;
    }
}