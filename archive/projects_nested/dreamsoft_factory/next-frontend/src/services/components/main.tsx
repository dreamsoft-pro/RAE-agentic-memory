import { useEffect } from 'react';
import axios from 'axios';

interface LayoutProps {
    children: JSX.Element;
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

// Define the API client interface
export const api = axios.create({
    baseURL: apiUrl,
});

const Header: React.FC<{ data: any }> = ({ data }) => (
    <header className="bg-blue-500 text-white p-4">
        <h1>{data.title}</h1>
        <nav>
            {data.navItems.map((item, index) => (
                <a key={index} href={item.url} className="ml-2 hover:underline">
                    {item.text}
                </a>
            ))}
        </nav>
    </header>
);

const Footer: React.FC<{ data: any }> = ({ data }) => (
    <footer className="bg-gray-100 p-4 text-center mt-auto">
        <p>{data.copyright}</p>
    </footer>
);

export default function Layout({ children }: LayoutProps) {
    const [headerData, setHeaderData] = React.useState(null);
    const [footerData, setFooterData] = React.useState(null);

    useEffect(() => {
        Promise.all([
            api.get('/api/header-data'),
            api.get('/api/footer-data')
        ]).then(responses => {
            if (responses[0].data && responses[1].data) {
                setHeaderData(responses[0].data);
                setFooterData(responses[1].data);
            }
        }).catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <>
            {headerData ? <Header data={headerData} /> : null}
            <div className="min-h-screen p-4">
                {children}
            </div>
            {footerData ? <Footer data={footerData} /> : null}
        </>
    );
}