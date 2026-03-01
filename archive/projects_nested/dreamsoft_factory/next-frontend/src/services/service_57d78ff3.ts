import React from 'react';
import api from '@/lib/api';  // Assuming this is your API wrapper

interface Product {
    id: number;
    name: string;
    formats?: string[];
}

interface SelectProductProps {
    product: Product;
    onFormatSelected(format: string): void;
}

class SelectProduct extends React.Component<SelectProductProps, { currentFormat: string }> {
    constructor(props: SelectProductProps) {
        super(props);
        this.state = {
            currentFormat: ''
        };
    }

    async selectFormat(format: string) {
        try {
            const url = `http://example.com/api/products/${this.props.product.id}/formats`;  // Example URL
            await api.put(url, { format });
            this.setState({ currentFormat: format });
            this.props.onFormatSelected(format);
        } catch (error) {
            console.error('Error selecting format:', error);
        }
    }

    render() {
        return (
            <div>
                <h2>Select Format for {this.props.product.name}</h2>
                <select onChange={(e) => this.selectFormat(e.target.value)}>
                    <option value="">Select a format</option>
                    {this.props.product.formats?.map(format => (
                        <option key={format} value={format}>{format}</option>
                    ))}
                </select>
            </div>
        );
    }
}

export default SelectProduct;