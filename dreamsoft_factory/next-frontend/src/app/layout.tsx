import '../globals.css';
import { RootLayout as LegacyRootLayout } from '../legacy_modules/RootLayout';

export const metadata = {
  title: 'Dreamsoft Pro 2.0',
  description: 'Zmodernizowany Frontend dla Dreamsoft',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pl">
      <body>
        <LegacyRootLayout>
          {children}
        </LegacyRootLayout>
      </body>
    </html>
  );
}