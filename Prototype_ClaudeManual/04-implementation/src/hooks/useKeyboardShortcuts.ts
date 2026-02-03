'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function useKeyboardShortcuts() {
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+K or Ctrl+K - Go to search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        router.push('/search');
      }

      // / - Focus navigation (if not in input)
      if (e.key === '/' && !isInputElement(e.target)) {
        e.preventDefault();
        const nav = document.querySelector('nav a') as HTMLElement;
        nav?.focus();
      }

      // ? - Show shortcuts help
      if (e.key === '?' && !isInputElement(e.target)) {
        e.preventDefault();
        router.push('/settings');
      }

      // Escape - Close modals or go back to home
      if (e.key === 'Escape') {
        const modal = document.querySelector('[role="dialog"]');
        if (modal) {
          // Close modal (implementation would need modal context)
          console.log('Close modal');
        } else {
          router.push('/');
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [router]);
}

function isInputElement(target: EventTarget | null): boolean {
  if (!target) return false;
  const element = target as HTMLElement;
  return (
    element.tagName === 'INPUT' ||
    element.tagName === 'TEXTAREA' ||
    element.contentEditable === 'true'
  );
}
