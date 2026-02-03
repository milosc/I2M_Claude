import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import { QueryProvider } from '@/providers/QueryProvider'
import { ThemeProvider } from '@/providers/ThemeProvider'
import { Navigation } from '@/components/Navigation'
import { KeyboardShortcuts } from '@/components/KeyboardShortcuts'
import '@/styles/globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'ClaudeManual - Framework Documentation Browser',
  description:
    'Browse skills, commands, agents, and architecture documentation for the HTEC Claude Code framework',
  keywords: ['Claude', 'AI', 'Framework', 'Documentation', 'Developer Tools'],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${jetbrainsMono.variable} font-mono antialiased`}>
        <ThemeProvider>
          <QueryProvider>
            <KeyboardShortcuts />
            <Navigation />
            {children}
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
