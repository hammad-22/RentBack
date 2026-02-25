import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RentBack — NYC Rent Negotiator",
  description: "Modern, data-driven rent negotiation for New York City.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <nav className="navbar">
          <div className="container navbar-inner">
            <a href="/" className="navbar-brand">
              <span className="brand-icon">⬡</span> RentBack
            </a>
            <div className="navbar-links">
              <a href="/">Overview</a>
              <a href="/analyze" className="btn btn-primary btn-sm">Start Analysis</a>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
