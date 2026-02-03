'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { SearchResultCard } from '@/components/SearchResultCard';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { TagFilter } from '@/components/TagFilter';
import { getAllUserTags, getComponentTags } from '@/lib/localStorage';
import Link from 'next/link';

interface SearchResult {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
  type: string;
  score?: number;
  tags?: string[];
}

async function fetchSearchResults(query: string): Promise<SearchResult[]> {
  const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Search failed');
  return response.json();
}

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const query = searchParams.get('q') || '';

  const [selectedStages, setSelectedStages] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [startTime] = useState(Date.now());

  // Load available tags on mount (PF-002)
  useEffect(() => {
    setAvailableTags(getAllUserTags());
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

  // Add user tags to results (PF-002)
  const resultsWithTags = (results || []).map((result) => ({
    ...result,
    tags: getComponentTags(result.id),
  }));

  // Filter results by stage and tags (PF-002)
  let filteredResults = resultsWithTags;

  if (selectedStages.length > 0) {
    filteredResults = filteredResults.filter((result) =>
      selectedStages.includes(result.stage)
    );
  }

  if (selectedTags.length > 0) {
    filteredResults = filteredResults.filter((result) =>
      result.tags && selectedTags.some((tag) => result.tags!.includes(tag))
    );
  }

  if (!query) {
    return (
      <main className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">Search Framework Components</h1>
          <p className="text-secondary">Enter a search query to get started</p>
          <Link href="/" className="text-accent-default hover:underline mt-4 inline-block">
            ← Back to Explorer
          </Link>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Searching for &quot;{query}&quot;...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-red-500 mb-4">Search failed. Please try again.</p>
          <Link href="/" className="text-accent-default hover:underline">
            ← Back to Explorer
          </Link>
        </div>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-6xl mx-auto">
          <Link href="/" className="text-accent-default hover:underline mb-4 inline-block">
            ← Back to Explorer
          </Link>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold">
                Search Results for &quot;{query}&quot;
              </h1>
              <p className="text-secondary text-sm">
                {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''} in{' '}
                {executionTime}s
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <StageFilterDropdown
              selectedStages={selectedStages as any}
              onChange={(stages) => setSelectedStages(stages as string[])}
            />
          </div>

          {/* Tag Filter (PF-002) */}
          {availableTags.length > 0 && (
            <div className="mt-4">
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
                Try different keywords or browse by stage
              </p>
              <Link href="/" className="text-accent-default hover:underline">
                Browse all components
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {filteredResults.map((result) => (
                <SearchResultCard
                  key={result.id}
                  result={{
                    id: result.id,
                    name: result.name,
                    type: (result.type || 'skill') as 'skill' | 'command' | 'agent' | 'rule' | 'hook',
                    stage: (result.stage?.toLowerCase() || 'discovery') as any,
                    path: result.path || '',
                    relevanceScore: result.score || 0,
                    summary: result.description || '',
                    tags: result.tags,
                    isFavorite: false,
                  }}
                  query={query}
                  onClick={() => router.push(`/?item=${result.id}`)}
                  onCopyPath={(path) => {
                    navigator.clipboard.writeText(path);
                  }}
                  onToggleFavorite={() => {
                    // Favorite functionality
                  }}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
