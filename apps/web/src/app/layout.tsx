import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'DATUMBIM Web Revit',
  description: 'Professional Web-Based BIM Workstation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-datumbim-bg text-datumbim-text">
        {children}
      </body>
    </html>
  )
}
