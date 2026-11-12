import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'HyperSettle — Institutional HyperCore FinOps & Settlement Engine',
  description:
    'Deterministic builder-code fee attribution, onchain HyperCore reconciliation, and Squads V4 Solana batch settlement export.'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#030706] text-[#eef6f4] antialiased">
        {children}
      </body>
    </html>
  );
}
