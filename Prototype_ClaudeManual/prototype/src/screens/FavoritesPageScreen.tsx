import React, { useState, useEffect } from 'react';
import {
  Button,
  Heading,
  Link,
  View,
  GridList,
  GridListItem,
  IllustratedMessage,
  Text,
} from '@/component-library';
import { ComponentCard } from '@/components/ComponentCard';
import { useNavigate } from 'react-router-dom';
import { useFavorites } from '@/hooks/useFavorites';
import { useToast } from '@/hooks/useToast';

interface FavoriteItem {
  id: string;
  type: 'Skill' | 'Command' | 'Agent';
  name: string;
  description: string;
  stage: string;
  path: string;
  model?: 'sonnet' | 'opus' | 'haiku';
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red';
}

/**
 * FavoritesPageScreen (SCR-004)
 *
 * Quick access panel for bookmarked frequently-used tools with drag-drop reordering.
 *
 * **Assembly-First**: Uses Adobe Spectrum React components (GridList, Button, IllustratedMessage)
 * and ClaudeManual aggregate component (ComponentCard).
 *
 * **Traceability**:
 * - PP-1.5 (Lack of Personalization)
 * - JTBD-1.6 (Bookmark tools for quick access)
 * - REQ-024 (Favorites persistence via localStorage)
 * - CF-012 (Favorites feature)
 *
 * **Data Flow**:
 * 1. Mount → Read favorites from localStorage
 * 2. Fetch full item details via /api/favorites?ids=...
 * 3. User reorders → Optimistic UI update → Persist to localStorage
 * 4. User removes → Optimistic UI update → Persist to localStorage
 *
 * **Keyboard Shortcuts**:
 * - Cmd+B: Open favorites (external, handled by AppRouter)
 * - Tab: Navigate between cards
 * - Enter: Activate focused button
 */
export function FavoritesPageScreen() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const {
    favorites,
    isLoading,
    error,
    removeFavorite,
    clearAllFavorites,
    reorderFavorites,
  } = useFavorites();

  const [isDragging, setIsDragging] = useState(false);
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  // Handle drag start
  const handleDragStart = () => {
    setIsDragging(true);
  };

  // Handle drag end
  const handleDragEnd = () => {
    setIsDragging(false);
  };

  // Handle reorder (GridList provides new order via onReorder)
  const handleReorder = async (newOrder: string[]) => {
    try {
      await reorderFavorites(newOrder);
      showToast('Favorites reordered', 'success');
    } catch (err) {
      showToast('Failed to reorder favorites', 'error');
    }
  };

  // Handle remove favorite
  const handleRemove = async (itemId: string) => {
    try {
      await removeFavorite(itemId);
      showToast('Removed from favorites', 'success');
    } catch (err) {
      showToast('Failed to remove favorite', 'error');
    }
  };

  // Handle clear all favorites
  const handleClearAll = async () => {
    try {
      await clearAllFavorites();
      setShowClearConfirm(false);
      showToast('All favorites cleared', 'success');
    } catch (err) {
      showToast('Failed to clear favorites', 'error');
    }
  };

  // Handle view details (navigate to Main Explorer with item selected)
  const handleView = (itemId: string) => {
    navigate(`/explorer?selected=${itemId}`);
  };

  // Handle copy path
  const handleCopyPath = async (path: string) => {
    try {
      await navigator.clipboard.writeText(path);
      showToast('Path copied to clipboard', 'success');
    } catch (err) {
      showToast('Failed to copy path', 'error');
    }
  };

  // Loading state
  if (isLoading) {
    return (
      <View padding="size-400">
        <Heading level={1}>Loading favorites...</Heading>
      </View>
    );
  }

  // Error state
  if (error) {
    return (
      <View padding="size-400">
        <IllustratedMessage>
          <Heading>Failed to load favorites</Heading>
          <Text>{error}</Text>
          <Button variant="primary" onPress={() => window.location.reload()}>
            Retry
          </Button>
        </IllustratedMessage>
      </View>
    );
  }

  // Empty state
  if (favorites.length === 0) {
    return (
      <View padding="size-400">
        <Link href="/explorer" variant="secondary">
          <Button variant="secondary">← Back to Explorer</Button>
        </Link>

        <View marginTop="size-600">
          <IllustratedMessage>
            <Heading>No favorites yet</Heading>
            <Text>
              Click the ⭐ icon on any skill, command, or agent to bookmark it for quick access.
            </Text>
            <Link href="/explorer">
              <Button variant="primary">Browse framework components</Button>
            </Link>
          </IllustratedMessage>
        </View>
      </View>
    );
  }

  // Populated state
  return (
    <View padding="size-400">
      {/* Header */}
      <View
        display="flex"
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        marginBottom="size-400"
      >
        <Link href="/explorer" variant="secondary">
          <Button variant="secondary">← Back to Explorer</Button>
        </Link>
      </View>

      <View
        display="flex"
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        marginBottom="size-600"
      >
        <Heading level={1}>My Favorites ({favorites.length} items)</Heading>
        <Button
          variant="negative"
          onPress={() => setShowClearConfirm(true)}
          isDisabled={favorites.length === 0}
        >
          Clear All
        </Button>
      </View>

      {/* Favorites Grid */}
      <GridList
        aria-label="Favorites grid"
        aria-describedby="drag-hint"
        selectionMode="none"
        items={favorites}
        onReorder={(keys) => {
          handleReorder(Array.from(keys) as string[]);
        }}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
        renderEmptyState={() => (
          <IllustratedMessage>
            <Heading>No favorites yet</Heading>
            <Text>Click ⭐ on any component to add it here.</Text>
          </IllustratedMessage>
        )}
        UNSAFE_className={`
          grid
          grid-cols-1
          md:grid-cols-2
          lg:grid-cols-3
          gap-6
          ${isDragging ? 'cursor-grabbing' : ''}
        `}
      >
        {(item) => (
          <GridListItem key={item.id} textValue={item.name}>
            <ComponentCard
              item={item}
              variant="compact"
              showFavoriteToggle={true}
              isFavorited={true}
              onView={() => handleView(item.id)}
              onCopyPath={() => handleCopyPath(item.path)}
              onToggleFavorite={() => handleRemove(item.id)}
            />
          </GridListItem>
        )}
      </GridList>

      {/* Drag hint (screen reader only) */}
      <Text id="drag-hint" UNSAFE_className="sr-only">
        Drag cards to reorder favorites. Changes save automatically.
      </Text>

      {/* Clear All Confirmation Dialog */}
      {showClearConfirm && (
        <div
          role="dialog"
          aria-labelledby="clear-confirm-title"
          aria-describedby="clear-confirm-desc"
          className="fixed inset-0 z-modal flex items-center justify-center bg-black/50"
          onClick={() => setShowClearConfirm(false)}
        >
          <div
            className="bg-surface-1 rounded-lg shadow-lg p-6 max-w-md"
            onClick={(e) => e.stopPropagation()}
          >
            <Heading id="clear-confirm-title" level={2}>
              Clear all favorites?
            </Heading>
            <Text id="clear-confirm-desc" marginTop="size-200">
              This will remove all {favorites.length} favorited items. This action cannot be undone.
            </Text>
            <View
              display="flex"
              direction="row"
              gap="size-200"
              marginTop="size-400"
              justifyContent="flex-end"
            >
              <Button variant="secondary" onPress={() => setShowClearConfirm(false)}>
                Cancel
              </Button>
              <Button variant="negative" onPress={handleClearAll}>
                Clear All
              </Button>
            </View>
          </div>
        </div>
      )}
    </View>
  );
}
