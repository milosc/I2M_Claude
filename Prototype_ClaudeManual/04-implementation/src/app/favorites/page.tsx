'use client';

import { useState, useEffect, useCallback } from 'react';
import { FavoritesPanel } from '@/components/FavoritesPanel';
import type { ComponentMeta } from '@/components/FavoritesPanel';
import { getPreferences, savePreferences } from '@/lib/localStorage';

interface FrameworkItem {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent';
  description: string;
  stage: string;
  path: string;
}

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<ComponentMeta[]>([]);
  const [favoriteIds, setFavoriteIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // Load favorite IDs and component data on mount
  useEffect(() => {
    async function loadFavorites() {
      try {
        const prefs = getPreferences();
        const ids = prefs.favorites || [];
        setFavoriteIds(ids);

        if (ids.length === 0) {
          setFavorites([]);
          setLoading(false);
          return;
        }

        // Fetch all components to get full data
        const [skillsRes, commandsRes, agentsRes] = await Promise.all([
          fetch('/api/skills'),
          fetch('/api/commands'),
          fetch('/api/agents'),
        ]);

        const skills: FrameworkItem[] = skillsRes.ok ? await skillsRes.json() : [];
        const commands: FrameworkItem[] = commandsRes.ok ? await commandsRes.json() : [];
        const agents: FrameworkItem[] = agentsRes.ok ? await agentsRes.json() : [];

        const allItems = [...skills, ...commands, ...agents];

        // Map favorite IDs to full component data
        const favoriteItems: ComponentMeta[] = ids
          .map((id) => {
            const item = allItems.find((i) => i.id === id);
            if (!item) return null;
            return {
              id: item.id,
              name: item.name,
              type: item.type as ComponentMeta['type'],
              stage: item.stage.toLowerCase() as ComponentMeta['stage'],
              path: item.path,
              summary: item.description,
              isFavorite: true,
            };
          })
          .filter((item): item is ComponentMeta => item !== null);

        setFavorites(favoriteItems);
      } catch (error) {
        console.error('Failed to load favorites:', error);
      } finally {
        setLoading(false);
      }
    }

    loadFavorites();
  }, []);

  const handleReorder = useCallback((newOrder: string[]) => {
    const reordered = newOrder
      .map((id) => favorites.find((f) => f.id === id))
      .filter((f): f is ComponentMeta => f !== undefined);
    setFavorites(reordered);
    // Update storage with new order
    savePreferences({ favorites: newOrder });
    setFavoriteIds(newOrder);
  }, [favorites]);

  const handleRemove = useCallback((componentId: string) => {
    setFavorites((prev) => prev.filter((f) => f.id !== componentId));
    const newIds = favoriteIds.filter((id) => id !== componentId);
    savePreferences({ favorites: newIds });
    setFavoriteIds(newIds);
  }, [favoriteIds]);

  const handleClearAll = useCallback(() => {
    setFavorites([]);
    savePreferences({ favorites: [] });
    setFavoriteIds([]);
  }, []);

  const handleClick = (componentId: string) => {
    // Navigate to component detail
    window.location.href = `/?detail=${componentId}`;
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Loading favorites...</p>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-4 py-3">
        <div className="flex items-center gap-4">
          <a href="/" className="text-accent-default hover:underline text-sm">
            ← Back to Explorer
          </a>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-6">
        <FavoritesPanel
          favorites={favorites}
          onReorder={handleReorder}
          onRemove={handleRemove}
          onClearAll={handleClearAll}
          onClick={handleClick}
        />
      </main>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-2 text-sm text-secondary">
        Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework
      </footer>
    </div>
  );
}
