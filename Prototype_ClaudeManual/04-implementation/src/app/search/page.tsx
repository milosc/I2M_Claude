'use client';

import { useState, useEffect, useMemo } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { SearchResultCard } from '@/components/SearchResultCard';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { TagFilter } from '@/components/TagFilter';
import { TypeFilter, ItemType } from '@/components/TypeFilter';
import { FileContentModal } from '@/components/FileContentModal';
import { getAllUserTags, getComponentTags } from '@/lib/localStorage';
import Link from 'next/link';

interface SearchResult {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Hook' | 'Workflow' | 'Architecture';
  tags?: string[];
  content?: string;
  score?: number;
}

async function fetchSearchResults(query: string): Promise<SearchResult[]> {
  const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Search failed');
  return response.json();
}

// Group results by type
function groupResultsByType(results: SearchResult[]): Record<string, SearchResult[]> {
  const groups: Record<string, SearchResult[]> = {};
  for (const result of results) {
    const type = result.type || 'Other';
    if (!groups[type]) {
      groups[type] = [];
    }
    groups[type].push(result);
  }
  return groups;
}

// Get counts per type
function getTypeCounts(results: SearchResult[]): Partial<Record<ItemType, number>> {
  const counts: Partial<Record<ItemType, number>> = {};
  for (const result of results) {
    const type = result.type as ItemType;
    counts[type] = (counts[type] || 0) + 1;
  }
  return counts;
}

// Extract unique tags from results
function extractTags(results: SearchResult[]): string[] {
  const tagSet = new Set<string>();
  for (const result of results) {
    if (result.tags) {
      for (const tag of result.tags) {
        tagSet.add(tag);
      }
    }
  }
  return Array.from(tagSet).sort();
}

// Type ordering for display
const TYPE_ORDER: ItemType[] = ['Skill', 'Command', 'Agent', 'Hook', 'Workflow', 'Architecture'];

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const query = searchParams.get('q') || '';

  const [selectedStages, setSelectedStages] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<ItemType[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [userTags, setUserTags] = useState<string[]>([]);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(TYPE_ORDER));
  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(null);
  const [startTime] = useState(Date.now());
  const [searchInput, setSearchInput] = useState(query);

  // Sync search input with URL query
  useEffect(() => {
    setSearchInput(query);
  }, [query]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchInput.trim())}`);
    }
  };

  // Load user tags on mount
  useEffect(() => {
    setUserTags(getAllUserTags());
  }, []);

  const {
    data: results,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetchSearchResults(query),
    enabled: !!query,
  });

  const executionTime = isLoading ? 0 : ((Date.now() - startTime) / 1000).toFixed(2);

  // Add user tags to results
  const resultsWithUserTags = useMemo(() => {
    return (results || []).map((result) => ({
      ...result,
      tags: [...(result.tags || []), ...getComponentTags(result.id)],
    }));
  }, [results]);

  // Filter results
  const filteredResults = useMemo(() => {
    let filtered = resultsWithUserTags;

    // Filter by stage
    if (selectedStages.length > 0) {
      filtered = filtered.filter((result) =>
        selectedStages.includes(result.stage.toLowerCase())
      );
    }

    // Filter by type
    if (selectedTypes.length > 0) {
      filtered = filtered.filter((result) =>
        selectedTypes.includes(result.type)
      );
    }

    // Filter by tags
    if (selectedTags.length > 0) {
      filtered = filtered.filter((result) =>
        result.tags && selectedTags.some((tag) => result.tags!.includes(tag))
      );
    }

    return filtered;
  }, [resultsWithUserTags, selectedStages, selectedTypes, selectedTags]);

  // Group filtered results
  const groupedResults = useMemo(() => groupResultsByType(filteredResults), [filteredResults]);

  // Type counts (before type filter applied)
  const typeCounts = useMemo(() => {
    let results = resultsWithUserTags;
    // Apply stage and tag filters but not type filter for counts
    if (selectedStages.length > 0) {
      results = results.filter((r) => selectedStages.includes(r.stage.toLowerCase()));
    }
    if (selectedTags.length > 0) {
      results = results.filter((r) => r.tags && selectedTags.some((tag) => r.tags!.includes(tag)));
    }
    return getTypeCounts(results);
  }, [resultsWithUserTags, selectedStages, selectedTags]);

  // Available tags from filtered results
  const availableTags = useMemo(() => {
    const fromResults = extractTags(filteredResults);
    return [...new Set([...fromResults, ...userTags])].sort();
  }, [filteredResults, userTags]);

  // Toggle section expansion
  const toggleSection = (type: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(type)) {
        next.delete(type);
      } else {
        next.add(type);
      }
      return next;
    });
  };

  // Handle result click - open modal
  const handleResultClick = (result: SearchResult) => {
    setSelectedFilePath(result.path);
  };

  // Handle modal close
  const handleModalClose = () => {
    setSelectedFilePath(null);
  };

  if (!query) {
    return (
      <main className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-3xl font-bold mb-6">Search Framework Components</h1>
          <p className="text-secondary mb-8">Search across Skills, Commands, Agents, Hooks, Workflows, and Architecture docs</p>

          <form onSubmit={handleSearch} className="mb-8">
            <div className="relative">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search by name, content, or tags..."
                className="w-full px-6 py-4 pl-12 text-lg bg-surface border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-accent-default focus:border-transparent"
                autoFocus
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-secondary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <button
                type="submit"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 px-4 py-2 bg-accent-default text-white rounded-lg hover:bg-accent-hover transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          <div className="text-sm text-secondary mb-4">
            Try searching for: <button onClick={() => { setSearchInput('discovery'); router.push('/search?q=discovery'); }} className="text-accent-default hover:underline mx-1">discovery</button> |
            <button onClick={() => { setSearchInput('prototype'); router.push('/search?q=prototype'); }} className="text-accent-default hover:underline mx-1">prototype</button> |
            <button onClick={() => { setSearchInput('quality'); router.push('/search?q=quality'); }} className="text-accent-default hover:underline mx-1">quality</button> |
            <button onClick={() => { setSearchInput('hook'); router.push('/search?q=hook'); }} className="text-accent-default hover:underline mx-1">hook</button>
          </div>

          <Link href="/" className="text-accent-default hover:underline mt-4 inline-block">
            &larr; Back to Explorer
          </Link>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="flex items-center gap-3">
          <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Searching for &quot;{query}&quot;...</span>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-red-500 mb-4">Search failed. Please try again.</p>
          <Link href="/" className="text-accent-default hover:underline">
            &larr; Back to Explorer
          </Link>
        </div>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-4 py-3 sticky top-0 bg-background z-10">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <Link href="/" className="text-accent-default hover:underline flex-shrink-0">
              &larr; Back
            </Link>

            {/* Search Input */}
            <form onSubmit={handleSearch} className="flex-1 max-w-xl">
              <div className="relative">
                <input
                  type="text"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  placeholder="Search..."
                  className="w-full px-4 py-2 pl-10 bg-surface border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-default focus:border-transparent"
                />
                <svg
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-secondary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </form>

            <p className="text-secondary text-sm flex-shrink-0">
              {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''} in {executionTime}s
            </p>
          </div>

          {/* Type Filter */}
          <div className="mb-4">
            <TypeFilter
              selectedTypes={selectedTypes}
              onChange={setSelectedTypes}
              counts={typeCounts}
            />
          </div>

          {/* Stage Filter */}
          <div className="flex items-center gap-4 mb-4">
            <StageFilterDropdown
              selectedStages={selectedStages as any}
              onChange={(stages) => setSelectedStages(stages as string[])}
            />
          </div>

          {/* Tag Filter */}
          {availableTags.length > 0 && (
            <div className="mt-2">
              <TagFilter
                availableTags={availableTags}
                selectedTags={selectedTags}
                onTagsChange={setSelectedTags}
                label="Filter by tags"
              />
            </div>
          )}
        </div>
      </header>

      {/* Results */}
      <main className="flex-1 px-4 py-6">
        <div className="max-w-6xl mx-auto">
          {filteredResults.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-secondary text-lg mb-4">
                No results found for &quot;{query}&quot;
              </p>
              <p className="text-sm text-secondary mb-6">
                Try different keywords or adjust your filters
              </p>
              <Link href="/" className="text-accent-default hover:underline">
                Browse all components
              </Link>
            </div>
          ) : (
            <div className="space-y-6">
              {TYPE_ORDER.filter((type) => groupedResults[type]?.length > 0).map((type) => {
                const typeResults = groupedResults[type];
                const isExpanded = expandedSections.has(type);

                return (
                  <section key={type} className="border border-border rounded-lg overflow-hidden">
                    {/* Section Header */}
                    <button
                      onClick={() => toggleSection(type)}
                      className="w-full flex items-center justify-between px-4 py-3 bg-surface hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <svg
                          className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                        <h2 className="text-lg font-semibold">{type}s</h2>
                        <span className="text-sm text-secondary">({typeResults.length})</span>
                      </div>
                    </button>

                    {/* Section Content */}
                    {isExpanded && (
                      <div className="divide-y divide-border">
                        {typeResults.map((result) => (
                          <div key={result.id} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                            <SearchResultCard
                              result={{
                                id: result.id,
                                name: result.name,
                                type: result.type.toLowerCase() as 'skill' | 'command' | 'agent' | 'rule' | 'hook',
                                stage: (result.stage?.toLowerCase() || 'discovery') as any,
                                path: result.path || '',
                                relevanceScore: result.score || 0,
                                summary: result.description || '',
                                tags: result.tags,
                                isFavorite: false,
                              }}
                              query={query}
                              onClick={() => handleResultClick(result)}
                              onCopyPath={(path) => {
                                navigator.clipboard.writeText(path);
                              }}
                              onToggleFavorite={() => {
                                // Favorite functionality
                              }}
                            />
                            {/* Show content preview if available */}
                            {result.content && (
                              <div className="mt-2 ml-12 text-sm text-secondary line-clamp-2">
                                {result.content.slice(0, 200)}...
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </section>
                );
              })}
            </div>
          )}
        </div>
      </main>

      {/* File Content Modal */}
      <FileContentModal
        filePath={selectedFilePath}
        onClose={handleModalClose}
      />
    </div>
  );
}
