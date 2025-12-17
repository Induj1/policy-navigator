import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Policy Navigator',
  description: 'Multi-agent AI system for government policy interpretation and benefit matching',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <nav className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-indigo-600">Policy Navigator</h1>
              </div>
              <div className="flex space-x-4">
                <a href="/" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Home</a>
                <a href="/citizen" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Check Eligibility</a>
                <a href="/policies" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Policies</a>
                <a href="/benefits" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">Benefits</a>
              </div>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}