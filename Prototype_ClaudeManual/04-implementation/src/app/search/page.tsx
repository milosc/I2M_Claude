'use client';

import { useState, useEffect, useMemo } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { SearchResultCard } from '@/components/SearchResultCard';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { TagFilter } from '@/components/TagFilter';
import { TypeFilter, ItemType } from '@/components/TypeFilter';
import { FileContentModal } from '@/components/FileContentModal';
import { AllTagsPanel, TagWithCount } from '@/components/AllTagsPanel';
import { getAllUserTags, getComponentTags, getPreferences } from '@/lib/localStorage';
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
  const tagParam = searchParams.get('tag') || '';

  const [selectedStages, setSelectedStages] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<ItemType[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [userTags, setUserTags] = useState<string[]>([]);
  const [allTagsWithCounts, setAllTagsWithCounts] = useState<TagWithCount[]>([]);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(TYPE_ORDER));
  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(null);
  const [startTime] = useState(Date.now());
  const [searchInput, setSearchInput] = useState(query);

  // Sync search input with URL query
  useEffect(() => {
    setSearchInput(query);
  }, [query]);

  // Sync tag filter from URL parameter
  useEffect(() => {
    if (tagParam) {
      const tags = tagParam.split(',').map((t) => t.trim()).filter(Boolean);
      if (tags.length > 0 && !tags.every((t) => selectedTags.includes(t))) {
        setSelectedTags((prev) => [...new Set([...prev, ...tags])]);
      }
    }
  }, [tagParam]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchInput.trim())}`);
    }
  };

  // Load user tags with counts on mount
  useEffect(() => {
    const tags = getAllUserTags();
    setUserTags(tags);

    // Calculate tag counts from component_tags
    const prefs = getPreferences();
    const tagCounts: Record<string, number> = {};
    Object.values(prefs.component_tags).forEach((componentTags) => {
      componentTags.forEach((tag) => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      });
    });

    const tagsWithCounts: TagWithCount[] = tags.map((tag) => ({
      name: tag,
      count: tagCounts[tag] || 0,
    }));
    setAllTagsWithCounts(tagsWithCounts);
  }, []);

  // Toggle tag selection
  const handleTagClick = (tag: string) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  // Clear all selected tags
  const handleClearAllTags = () => {
    setSelectedTags([]);
  };

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
          <p className="text-gray-600 mb-8">Search across Skills, Commands, Agents, Hooks, Workflows, and Architecture docs</p>

          <form onSubmit={handleSearch} className="mb-8">
            <div className="relative">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search by name, content, or tags..."
                className="w-full px-6 py-4 pl-12 text-lg text-gray-900 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                autoFocus
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <button
                type="submit"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          <div className="text-sm text-gray-600 mb-4">
            Try searching for: <button onClick={() => { setSearchInput('discovery'); router.push('/search?q=discovery'); }} className="text-blue-600 hover:underline mx-1">discovery</button> |
            <button onClick={() => { setSearchInput('prototype'); router.push('/search?q=prototype'); }} className="text-blue-600 hover:underline mx-1">prototype</button> |
            <button onClick={() => { setSearchInput('quality'); router.push('/search?q=quality'); }} className="text-blue-600 hover:underline mx-1">quality</button> |
            <button onClick={() => { setSearchInput('hook'); router.push('/search?q=hook'); }} className="text-blue-600 hover:underline mx-1">hook</button>
          </div>

          {/* All Tags Panel - always shown on empty search page */}
          <div className="mt-8 max-w-lg mx-auto">
            {allTagsWithCounts.length > 0 ? (
              <AllTagsPanel
                tags={allTagsWithCounts}
                selectedTags={selectedTags}
                onTagClick={(tag) => {
                  // When clicking a tag on empty page, search for it
                  handleTagClick(tag);
                  router.push(`/search?q=*&tag=${encodeURIComponent(tag)}`);
                }}
                onClearAll={handleClearAllTags}
                collapsible={false}
                title="Browse by Tag"
              />
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
                <h3 className="font-semibold text-gray-800 mb-2">Browse by Tag</h3>
                <p className="text-sm text-gray-600">
                  No tags yet. Add tags to components from the detail pane to see them here.
                </p>
              </div>
            )}
          </div>

          <Link href="/" className="text-blue-600 hover:underline mt-6 inline-block">
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
          <span>{query === '*' ? 'Loading all components...' : `Searching for "${query}"...`}</span>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-red-500 mb-4">Search failed. Please try again.</p>
          <Link href="/" className="text-blue-600 hover:underline">
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
            <Link href="/" className="text-blue-600 hover:underline flex-shrink-0">
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
                  className="w-full px-4 py-2 pl-10 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <svg
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </form>

            <p className="text-gray-600 text-sm flex-shrink-0">
              {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''}
              {query === '*' ? ' (all components)' : ''} in {executionTime}s
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

          {/* All Tags Panel - collapsible on results page */}
          {allTagsWithCounts.length > 0 && (
            <div className="mt-3">
              <AllTagsPanel
                tags={allTagsWithCounts}
                selectedTags={selectedTags}
                onTagClick={handleTagClick}
                onClearAll={handleClearAllTags}
                collapsible={true}
                defaultCollapsed={true}
                title="All Tags"
              />
            </div>
          )}

          {/* Tag Filter - shows tags from current results */}
          {availableTags.length > 0 && selectedTags.length === 0 && (
            <div className="mt-2">
              <TagFilter
                availableTags={availableTags}
                selectedTags={selectedTags}
                onTagsChange={setSelectedTags}
                label="Filter by tags in results"
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
              <p className="text-gray-600 text-lg mb-4">
                {query === '*'
                  ? 'No components match the selected filters'
                  : `No results found for "${query}"`}
              </p>
              <p className="text-sm text-gray-600 mb-6">
                {selectedTags.length > 0
                  ? 'Try removing some tag filters'
                  : 'Try different keywords or adjust your filters'}
              </p>
              {selectedTags.length > 0 && (
                <button
                  onClick={handleClearAllTags}
                  className="text-blue-600 hover:underline mr-4"
                >
                  Clear tag filters
                </button>
              )}
              <Link href="/" className="text-blue-600 hover:underline">
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
                      className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
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
                        <span className="text-sm text-gray-600">({typeResults.length})</span>
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
                              <div className="mt-2 ml-12 text-sm text-gray-600 line-clamp-2">
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
