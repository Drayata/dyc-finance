import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MarketPulse AI — Market Intelligence Platform",
  description:
    "AI-powered market intelligence platform for stocks and cryptocurrencies. Transparent, evidence-based analytical signals for educational and market-analysis purposes.",
  keywords: ["market intelligence", "stock analysis", "crypto analysis", "AI signals", "market data"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="dark" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="antialiased">
        {/* Demo Mode Banner */}
        {process.env.NEXT_PUBLIC_DEMO_MODE === "true" && (
          <div className="demo-banner" role="alert">
            ⚠️ DEMO MODE — All data shown is simulated for demonstration purposes. Not real market data.
          </div>
        )}
        {children}
      </body>
    </html>
  );
}
