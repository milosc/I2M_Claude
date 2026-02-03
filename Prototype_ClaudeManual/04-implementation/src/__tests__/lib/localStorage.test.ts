import { describe, it, expect, beforeEach, vi } from 'vitest'
import {
  getPreferences,
  savePreferences,
  addFavorite,
  removeFavorite,
  toggleFavorite,
  isFavorited,
  addSearchHistory,
  clearSearchHistory,
  setTheme,
  toggleStageFilter,
  clearFilters,
  resetPreferences,
} from '@/lib/localStorage'
import { Theme, Stage } from '@/types'

describe('localStorage utilities', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    vi.clearAllMocks()
  })

  describe('getPreferences', () => {
    it('returns default preferences when localStorage is empty', () => {
      const prefs = getPreferences()

      expect(prefs.theme).toBe(Theme.System)
      expect(prefs.favorites).toEqual([])
      expect(prefs.collapsed_nodes).toEqual([])
      expect(prefs.last_viewed).toBeNull()
      expect(prefs.search_history).toEqual([])
      expect(prefs.stage_filter).toEqual([])
      expect(prefs.type_filter).toEqual([])
    })

    it('returns stored preferences when they exist', () => {
      const storedPrefs = {
        theme: Theme.Dark,
        favorites: ['skill-1', 'command-2'],
        collapsed_nodes: ['node-1'],
        last_viewed: 'skill-1',
        search_history: ['test'],
        stage_filter: [Stage.Discovery],
        type_filter: ['Skill'],
      }

      localStorage.setItem('claudemanual-preferences', JSON.stringify(storedPrefs))

      const prefs = getPreferences()
      expect(prefs).toEqual(storedPrefs)
    })

    it('returns defaults on parse error', () => {
      localStorage.setItem('claudemanual-preferences', 'invalid-json')

      const prefs = getPreferences()
      expect(prefs.theme).toBe(Theme.System)
    })
  })

  describe('savePreferences', () => {
    it('saves preferences to localStorage', () => {
      savePreferences({ theme: Theme.Dark })

      const stored = localStorage.getItem('claudemanual-preferences')
      expect(stored).toBeTruthy()

      const parsed = JSON.parse(stored!)
      expect(parsed.theme).toBe(Theme.Dark)
    })

    it('merges with existing preferences', () => {
      savePreferences({ theme: Theme.Dark })
      savePreferences({ favorites: ['skill-1'] })

      const prefs = getPreferences()
      expect(prefs.theme).toBe(Theme.Dark)
      expect(prefs.favorites).toEqual(['skill-1'])
    })
  })

  describe('favorites', () => {
    it('adds item to favorites', () => {
      addFavorite('skill-1')

      const prefs = getPreferences()
      expect(prefs.favorites).toContain('skill-1')
    })

    it('does not add duplicate favorites', () => {
      addFavorite('skill-1')
      addFavorite('skill-1')

      const prefs = getPreferences()
      expect(prefs.favorites).toEqual(['skill-1'])
    })

    it('removes item from favorites', () => {
      addFavorite('skill-1')
      addFavorite('skill-2')
      removeFavorite('skill-1')

      const prefs = getPreferences()
      expect(prefs.favorites).toEqual(['skill-2'])
    })

    it('toggles favorite status', () => {
      toggleFavorite('skill-1')
      expect(isFavorited('skill-1')).toBe(true)

      toggleFavorite('skill-1')
      expect(isFavorited('skill-1')).toBe(false)
    })
  })

  describe('search history', () => {
    it('adds query to search history', () => {
      addSearchHistory('test query')

      const prefs = getPreferences()
      expect(prefs.search_history).toContain('test query')
    })

    it('moves duplicate query to top of history', () => {
      addSearchHistory('query 1')
      addSearchHistory('query 2')
      addSearchHistory('query 1')

      const prefs = getPreferences()
      expect(prefs.search_history[0]).toBe('query 1')
      expect(prefs.search_history).toHaveLength(2)
    })

    it('limits search history to 10 items', () => {
      for (let i = 0; i < 15; i++) {
        addSearchHistory(`query ${i}`)
      }

      const prefs = getPreferences()
      expect(prefs.search_history).toHaveLength(10)
    })

    it('clears search history', () => {
      addSearchHistory('test')
      clearSearchHistory()

      const prefs = getPreferences()
      expect(prefs.search_history).toEqual([])
    })
  })

  describe('theme', () => {
    it('sets theme preference', () => {
      setTheme(Theme.Dark)

      const prefs = getPreferences()
      expect(prefs.theme).toBe(Theme.Dark)
    })
  })

  describe('filters', () => {
    it('toggles stage filter', () => {
      toggleStageFilter(Stage.Discovery)

      let prefs = getPreferences()
      expect(prefs.stage_filter).toContain(Stage.Discovery)

      toggleStageFilter(Stage.Discovery)

      prefs = getPreferences()
      expect(prefs.stage_filter).not.toContain(Stage.Discovery)
    })

    it('clears all filters', () => {
      toggleStageFilter(Stage.Discovery)
      clearFilters()

      const prefs = getPreferences()
      expect(prefs.stage_filter).toEqual([])
      expect(prefs.type_filter).toEqual([])
    })
  })

  describe('resetPreferences', () => {
    it('removes preferences from localStorage', () => {
      savePreferences({ theme: Theme.Dark })
      resetPreferences()

      const stored = localStorage.getItem('claudemanual-preferences')
      expect(stored).toBeNull()
    })
  })
})
