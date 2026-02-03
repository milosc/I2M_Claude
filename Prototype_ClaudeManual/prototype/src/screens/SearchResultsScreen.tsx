import React, { useState, useEffect, useCallback } from 'react';
import {
  Heading,
  View,
  Text,
  Link,
  Button,
  TextField,
  Select,
  Item,
  ProgressCircle,
  IllustratedMessage,
  Content,
} from '@/component-library';
import { SearchResultCard } from '@/components/SearchResultCard';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useDebounce } from '@/hooks/useDebounce';

interface SearchResult {
  id: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc';
  name: string;
  description: string;
  stage?: string;
  path: string;
  score: number;
  highlights?: {
    name?: string;
    description?: string;
  };
}

interface SearchResponse {
  results: SearchResult[];
  pagination: {
    page: number;
    pageSize: number;
    totalResults: number;
    totalPages: number;
    hasMore: boolean;
  };
  performanceMetrics: {
    executionTime: number;
    indexedItems: number;
  };
}

type SortOption = 'relevance' | 'alphabetical' | 'recent';

export function SearchResultsScreen() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // Extract query from URL
  const initialQuery = searchParams.get('q') || '';

  // State
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedStages, setSelectedStages] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<SortOption>('relevance');
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 20,
    totalResults: 0,
    totalPages: 0,
    hasMore: false,
  });
  const [performanceMetrics, setPerformanceMetrics] = useState({
    executionTime: 0,
    indexedItems: 0,
  });

  // Debounce query for search
  const debouncedQuery = useDebounce(query, 300);

  // Fetch search results
  const fetchResults = useCallback(async (searchQuery: string, page = 1) => {
    if (searchQuery.length < 2) {
      setResults([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          types: selectedTypes.length > 0 ? selectedTypes : undefined,
          stages: selectedStages.length > 0 ? selectedStages : undefined,
          sortBy,
          page,
          pageSize: 20,
        }),
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data: SearchResponse = await response.json();

      if (page === 1) {
        setResults(data.results);
      } else {
        setResults(prev => [...prev, ...data.results]);
      }

      setPagination(data.pagination);
      setPerformanceMetrics(data.performanceMetrics);

      // Update search history in localStorage
      const searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
      if (!searchHistory.includes(searchQuery)) {
        searchHistory.unshift(searchQuery);
        if (searchHistory.length > 20) searchHistory.pop();
        localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
      }
    } catch (err) {
      setError('Search temporarily unavailable. Try browsing by category instead.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [selectedTypes, selectedStages, sortBy]);

  // Trigger search when debounced query changes
  useEffect(() => {
    if (debouncedQuery) {
      fetchResults(debouncedQuery);
      // Update URL
      setSearchParams({ q: debouncedQuery });
    }
  }, [debouncedQuery, fetchResults, setSearchParams]);

  // Load favorites from localStorage
  const [favorites, setFavorites] = useState<string[]>(() => {
    try {
      const prefs = JSON.parse(localStorage.getItem('userPreferences') || '{}');
      return prefs.favorites || [];
    } catch {
      return [];
    }
  });

  // Handle favorite toggle
  const handleFavoriteToggle = (resultId: string) => {
    const newFavorites = favorites.includes(resultId)
      ? favorites.filter(id => id !== resultId)
      : [...favorites, resultId];

    setFavorites(newFavorites);

    // Update localStorage
    const prefs = JSON.parse(localStorage.getItem('userPreferences') || '{}');
    prefs.favorites = newFavorites;
    localStorage.setItem('userPreferences', JSON.stringify(prefs));
  };

  // Handle copy path
  const handleCopyPath = (path: string) => {
    navigator.clipboard.writeText(path);
    // TODO: Show toast notification
  };

  // Handle view details
  const handleViewDetails = (resultId: string) => {
    navigate(`/?selected=${resultId}`);
  };

  // Load more results
  const handleLoadMore = () => {
    if (pagination.hasMore) {
      fetchResults(query, pagination.page + 1);
    }
  };

  // Performance indicator color
  const getPerformanceColor = () => {
    const timeInSeconds = performanceMetrics.executionTime / 1000;
    if (timeInSeconds < 1) return 'green';
    if (timeInSeconds < 2) return 'yellow';
    return 'red';
  };

  // Filtered results (client-side filtering)
  const filteredResults = results.filter(result => {
    if (selectedTypes.length > 0 && !selectedTypes.includes(result.type)) return false;
    if (selectedStages.length > 0 && result.stage && !selectedStages.includes(result.stage)) return false;
    return true;
  });

  return (
    <View className="min-h-screen bg-canvas">
      {/* Back Button */}
      <View className="px-6 py-4">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
        >
          <span aria-hidden="true">←</span>
          <span>Back to Explorer</span>
        </Link>
      </View>

      {/* Results Header */}
      <View className="px-6 py-4 border-b border-border-default">
        <Heading level={1} className="text-2xl font-semibold text-text-primary mb-2">
          {query ? `Search Results for "${query}"` : 'Search'}
        </Heading>
        {!loading && performanceMetrics.executionTime > 0 && (
          <Text className="text-sm text-text-secondary">
            <span className={`inline-block w-2 h-2 rounded-full mr-2 bg-${getPerformanceColor()}-500`} />
            {pagination.totalResults} results in &lt;{(performanceMetrics.executionTime / 1000).toFixed(2)}s
          </Text>
        )}
      </View>

      {/* Filters Bar */}
      <View className="px-6 py-4 border-b border-border-default flex flex-wrap gap-4 items-center">
        <StageFilterDropdown
          selectedStages={selectedStages}
          onChange={setSelectedStages}
        />

        <Select
          label="Type"
          selectedKey={selectedTypes.length === 1 ? selectedTypes[0] : 'all'}
          onSelectionChange={(key) => {
            if (key === 'all') {
              setSelectedTypes([]);
            } else {
              setSelectedTypes([key as string]);
            }
          }}
          className="min-w-[150px]"
        >
          <Item key="all">All Types</Item>
          <Item key="Skill">Skill</Item>
          <Item key="Command">Command</Item>
          <Item key="Agent">Agent</Item>
          <Item key="Rule">Rule</Item>
          <Item key="Hook">Hook</Item>
          <Item key="Workflow">Workflow</Item>
          <Item key="WaysOfWorking">Ways of Working</Item>
          <Item key="ArchitectureDoc">Architecture Doc</Item>
        </Select>

        <Select
          label="Sort by"
          selectedKey={sortBy}
          onSelectionChange={(key) => setSortBy(key as SortOption)}
          className="min-w-[150px]"
        >
          <Item key="relevance">Relevance</Item>
          <Item key="alphabetical">Alphabetical A-Z</Item>
          <Item key="recent">Recently Updated</Item>
        </Select>
      </View>

      {/* Results List */}
      <View className="px-6 py-6">
        {loading && pagination.page === 1 && (
          <View className="flex justify-center items-center py-12">
            <ProgressCircle aria-label="Loading results" isIndeterminate />
            <Text className="mt-4 text-text-secondary">Searching...</Text>
          </View>
        )}

        {error && (
          <IllustratedMessage>
            <Heading>Search Unavailable</Heading>
            <Content>{error}</Content>
            <Link href="/stage-filter?stage=Discovery">Browse by Stage</Link>
          </IllustratedMessage>
        )}

        {!loading && !error && query.length < 2 && (
          <View className="text-center py-12">
            <Text className="text-text-secondary text-lg">
              Type to search skills, commands, agents, or rules...
            </Text>
          </View>
        )}

        {!loading && !error && query.length >= 2 && filteredResults.length === 0 && (
          <IllustratedMessage>
            <Heading>No Results</Heading>
            <Content>
              No results for "{query}". Try different keywords or browse by stage.
            </Content>
            <Link href="/stage-filter?stage=Discovery">Browse by Stage</Link>
          </IllustratedMessage>
        )}

        {!loading && !error && filteredResults.length > 0 && (
          <View className="space-y-4">
            {filteredResults.map((result) => (
              <SearchResultCard
                key={result.id}
                id={result.id}
                name={result.name}
                description={result.description}
                type={result.type}
                stage={result.stage}
                path={result.path}
                isFavorite={favorites.includes(result.id)}
                onFavorite={() => handleFavoriteToggle(result.id)}
                onCopyPath={() => handleCopyPath(result.path)}
                onViewDetails={() => handleViewDetails(result.id)}
                highlights={result.highlights}
              />
            ))}
          </View>
        )}

        {/* Load More Button */}
        {!loading && pagination.hasMore && (
          <View className="mt-8 flex justify-center">
            <Button
              onPress={handleLoadMore}
              variant="secondary"
              className="px-6"
            >
              Load More Results
            </Button>
          </View>
        )}

        {loading && pagination.page > 1 && (
          <View className="mt-8 flex justify-center">
            <ProgressCircle aria-label="Loading more results" isIndeterminate size="S" />
          </View>
        )}
      </View>
    </View>
  );
}
