import { NextResponse } from 'next/server';

// Mock architecture documentation data
const mockArchitectureDocs = [
  {
    id: 'c4-001',
    name: 'Context Diagram',
    description: 'System context showing external actors and systems',
    format: 'mermaid' as const,
    category: 'c4' as const,
    c4_level: 'context' as const,
    content: {
      overview: 'Shows ClaudeManual system in context with external actors and systems.',
      diagram: `graph TB
    User[Framework User] --> System[ClaudeManual System]
    System --> FileSystem[File System]
    System --> ClaudeAPI[Claude API]`,
    },
  },
  {
    id: 'c4-002',
    name: 'Container Diagram',
    description: 'High-level containers and their interactions',
    format: 'mermaid' as const,
    category: 'c4' as const,
    c4_level: 'container' as const,
    content: {
      overview: 'Shows major containers: Web UI, API, File Watcher, and storage.',
      diagram: `graph TB
    User[User] --> WebUI[Web UI<br/>Next.js]
    WebUI --> API[API Routes<br/>Next.js API]
    API --> FS[File System<br/>Local Storage]
    API --> Cache[Cache<br/>localStorage]`,
    },
  },
  {
    id: 'adr-001',
    name: 'ADR-001: Next.js App Router',
    description: 'Decision to use Next.js 14 with App Router',
    format: 'md' as const,
    category: 'adr' as const,
    adr_status: 'accepted' as const,
    content: {
      overview: 'We chose Next.js App Router for better performance and developer experience.',
      decision: `## Decision

We will use Next.js 14 with the App Router (not Pages Router).

## Rationale

- Better performance with React Server Components
- Improved routing with nested layouts
- Built-in loading and error states
- Stronger TypeScript integration

## Consequences

- Requires React 18+
- Learning curve for team members familiar with Pages Router
- Some libraries may not support RSC yet`,
    },
    related_adrs: ['adr-002'],
  },
  {
    id: 'adr-002',
    name: 'ADR-002: TanStack Query',
    description: 'Use TanStack Query for data fetching',
    format: 'md' as const,
    category: 'adr' as const,
    adr_status: 'accepted' as const,
    content: {
      overview: 'TanStack Query provides robust caching and state management for server state.',
      decision: `## Decision

We will use TanStack Query (React Query) for all API data fetching.

## Rationale

- Built-in caching and deduplication
- Automatic background refetching
- Optimistic updates support
- Better error handling than raw fetch

## Consequences

- Additional dependency (~40KB)
- Team needs to learn Query patterns
- Consistent data fetching across app`,
    },
    related_adrs: ['adr-001', 'adr-003'],
  },
  {
    id: 'adr-003',
    name: 'ADR-003: Tailwind CSS',
    description: 'Use Tailwind CSS for styling',
    format: 'md' as const,
    category: 'adr' as const,
    adr_status: 'accepted' as const,
    content: {
      overview: 'Tailwind CSS provides utility-first styling with design tokens.',
      decision: `## Decision

We will use Tailwind CSS for all component styling.

## Rationale

- Utility-first approach reduces CSS bundle size
- Design tokens configured via tailwind.config.js
- Excellent IntelliSense support in VS Code
- No CSS-in-JS runtime overhead

## Consequences

- HTML markup has many class names
- Team needs to learn utility class patterns
- Highly consistent styling across components`,
    },
    related_adrs: ['adr-002'],
  },
  {
    id: 'pat-001',
    name: 'Repository Pattern',
    description: 'Data access abstraction pattern',
    format: 'md' as const,
    category: 'patterns' as const,
    content: {
      overview: 'Use repository pattern to abstract data sources and enable easy mocking.',
    },
  },
  {
    id: 'inf-001',
    name: 'Deployment Architecture',
    description: 'Static site deployment on Vercel',
    format: 'md' as const,
    category: 'infrastructure' as const,
    content: {
      overview: 'Static site export deployed to Vercel with edge caching.',
    },
  },
];

export async function GET() {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 100));

  return NextResponse.json(mockArchitectureDocs);
}
