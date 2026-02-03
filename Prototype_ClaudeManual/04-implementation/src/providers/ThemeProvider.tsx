'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { Theme } from '@/types'
import { getPreferences, setTheme as saveTheme } from '@/lib/localStorage'

interface ThemeContextType {
  theme: Theme
  effectiveTheme: 'light' | 'dark'
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(Theme.System)
  const [effectiveTheme, setEffectiveTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    // Load theme from localStorage
    const prefs = getPreferences()
    setThemeState(prefs.theme)
  }, [])

  useEffect(() => {
    // Calculate effective theme
    let effective: 'light' | 'dark' = 'light'

    if (theme === Theme.System) {
      effective = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    } else {
      effective = theme === Theme.Dark ? 'dark' : 'light'
    }

    setEffectiveTheme(effective)

    // Apply theme to document
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(effective)
  }, [theme])

  useEffect(() => {
    // Listen to system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

    const handleChange = () => {
      if (theme === Theme.System) {
        const effective = mediaQuery.matches ? 'dark' : 'light'
        setEffectiveTheme(effective)
        const root = window.document.documentElement
        root.classList.remove('light', 'dark')
        root.classList.add(effective)
      }
    }

    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [theme])

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme)
    saveTheme(newTheme)
  }

  return (
    <ThemeContext.Provider value={{ theme, effectiveTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}
