'use client';

import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

export function KeyboardShortcuts() {
  useKeyboardShortcuts();
  return null; // This component only sets up event listeners
}
