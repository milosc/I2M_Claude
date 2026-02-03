'use client'

/**
 * TagInput Component
 *
 * Autocomplete input for adding tags to components.
 * Shows existing tags as suggestions and allows creating new ones.
 *
 * Traceability:
 * - JTBD-1.3: Quickly Find Relevant Framework Tools - "Can tag components"
 * - CF-010: Tagging system
 * - PF-002: Tagging Feature Feedback
 */

import { useState, useRef, useEffect, KeyboardEvent } from 'react'

export interface TagInputProps {
  /** Tags currently applied to this component */
  currentTags: string[]
  /** All available tags for autocomplete suggestions */
  suggestedTags?: string[]
  /** Callback when user adds a new tag */
  onAddTag: (tag: string) => void
  /** Placeholder text */
  placeholder?: string
  /** Aria label for accessibility */
  label?: string
  /** Disable input */
  isDisabled?: boolean
}

export function TagInput({
  currentTags,
  suggestedTags = [],
  onAddTag,
  placeholder = 'Add tag...',
  label = 'Add tag',
  isDisabled = false,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const suggestionsRef = useRef<HTMLUListElement>(null)

  // Filter suggestions to exclude already-applied tags
  const availableSuggestions = [...new Set([...suggestedTags])]
    .filter((tag) => !currentTags.includes(tag))
    .filter((tag) => tag.toLowerCase().includes(inputValue.toLowerCase()))
    .slice(0, 8) // Limit to 8 suggestions

  const handleAddTag = (value: string) => {
    const trimmed = value.trim().toLowerCase()
    if (trimmed && !currentTags.includes(trimmed)) {
      onAddTag(trimmed)
      setInputValue('')
      setShowSuggestions(false)
      setSelectedIndex(-1)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      if (selectedIndex >= 0 && availableSuggestions[selectedIndex]) {
        handleAddTag(availableSuggestions[selectedIndex])
      } else if (inputValue.trim()) {
        handleAddTag(inputValue)
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSelectedIndex((prev) =>
        prev < availableSuggestions.length - 1 ? prev + 1 : prev
      )
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1))
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
      setSelectedIndex(-1)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value)
    setShowSuggestions(true)
    setSelectedIndex(-1)
  }

  const handleSuggestionClick = (tag: string) => {
    handleAddTag(tag)
    inputRef.current?.focus()
  }

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        inputRef.current &&
        !inputRef.current.contains(e.target as Node) &&
        suggestionsRef.current &&
        !suggestionsRef.current.contains(e.target as Node)
      ) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="tag-input-container relative">
      <label htmlFor="tag-input" className="sr-only">
        {label}
      </label>
      <input
        ref={inputRef}
        id="tag-input"
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onFocus={() => setShowSuggestions(true)}
        placeholder={placeholder}
        disabled={isDisabled}
        autoComplete="off"
        className="w-48 px-3 py-1.5 text-sm border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
        aria-describedby="tag-input-help"
        aria-expanded={showSuggestions && availableSuggestions.length > 0}
        aria-haspopup="listbox"
        aria-autocomplete="list"
      />

      {/* Suggestions dropdown */}
      {showSuggestions && availableSuggestions.length > 0 && (
        <ul
          ref={suggestionsRef}
          role="listbox"
          className="absolute z-10 mt-1 w-48 max-h-48 overflow-auto bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md shadow-lg"
        >
          {availableSuggestions.map((tag, index) => (
            <li
              key={tag}
              role="option"
              aria-selected={index === selectedIndex}
              onClick={() => handleSuggestionClick(tag)}
              className={`px-3 py-2 text-sm cursor-pointer ${
                index === selectedIndex
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100'
                  : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'
              }`}
            >
              {tag}
            </li>
          ))}
        </ul>
      )}

      <p id="tag-input-help" className="sr-only">
        Type and press Enter to add a new tag, or select from suggestions.
      </p>
    </div>
  )
}

export default TagInput
