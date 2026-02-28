import api from "@/lib/api";
import { useEffect, useState } from "react";

export default function ProductFormatSelector() {
    const [product, setProduct] = useState<{ currentFormat?: any; info: any }>({});
    
    useEffect(() => {
        async function fetchAndValidateFormat(searchFormat: any) {
            if (searchFormat) {
                product.currentFormat = searchFormat;
                
                if (!!searchFormat.custom) {
                    product.currentFormat.customWidth = searchFormat.minWidth - searchFormat.slope * 2;
                    product.currentFormat.customHeight = searchFormat.minHeight - searchFormat.slope * 2;
                }
            }

            if (!product.currentFormat) {
                Notification.error('not_related_format_for_product' + ' - ' + product.info.typeName);
                throw new Error("select another format");
            } else {
                setProduct(product); // Update state with validated and possibly modified currentFormat
            }
        }

        async function fetchData() {
            try {
                const searchFormat = await api.get('/search-format'); // Assuming an API call to fetch the search format
                await fetchAndValidateFormat(searchFormat);
            } catch (error) {
                Notification.error('Error fetching or validating format');
                console.error(error);                
            }
        }

        fetchData();
    }, []);

    return (
        <div>
            {/* Render your product component here */}
        </div>
    );
}

// Assuming a global Notification object is available in the context of this application
function Notification(message: string) {
    console.log('Notification:', message);
}