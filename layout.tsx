import "@/styles.css";

export const metadata = {
    title: 'Legal AI',
    description: 'AI-powered contract analysis',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
