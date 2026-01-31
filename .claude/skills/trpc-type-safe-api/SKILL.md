---
name: trpc-type-safe-api
description: Build end-to-end type-safe APIs with tRPC and TypeScript, eliminating code generation and runtime bloat for full-stack applications.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill trpc-type-safe-api started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill trpc-type-safe-api ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill trpc-type-safe-api instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# tRPC Type-Safe API Builder Skill

## What This Skill Enables

Claude can build fully type-safe APIs using tRPC (TypeScript Remote Procedure Call), part of the T3 Stack explosion in 2025. tRPC provides end-to-end type safety without code generation, schema stitching, or serialization layers - delivering a lighter, more intuitive developer experience than REST or GraphQL. With zero dependencies, tiny client-side footprint, and automatic type inference, tRPC makes full-stack TypeScript development actually enjoyable.

## Prerequisites

**Required:**
- Claude Pro subscription or Claude Code CLI  
- Node.js 18+ with TypeScript 5.0+
- Understanding of React or Next.js
- Basic API development knowledge

**What Claude handles automatically:**
- Setting up tRPC server with Express, Next.js, or standalone
- Creating type-safe routers and procedures
- Implementing middleware for authentication
- Generating React Query hooks automatically
- Adding input validation with Zod
- Configuring error handling and transformers
- Setting up WebSocket subscriptions
- Integrating with Prisma or other ORMs

## How to Use This Skill

### Create Basic tRPC API

**Prompt:** "Set up a tRPC API with Next.js 15 that has procedures for creating, reading, updating, and deleting todos. Include Zod validation and automatic React Query hooks."

Claude will:
1. Initialize tRPC router with type-safe procedures
2. Add Zod schemas for input validation
3. Create CRUD operations with proper types
4. Set up Next.js API route handlers
5. Generate React hooks for client usage
6. Include error handling and transformers
7. Add TypeScript types exported automatically

### Authentication Middleware

**Prompt:** "Add JWT authentication middleware to my tRPC API. Protected procedures should verify the token and attach user data to context."

Claude will:
1. Create authentication middleware
2. Verify JWT tokens with jose library
3. Extend tRPC context with user data
4. Create protected procedure wrapper
5. Add type-safe context typing
6. Include refresh token logic
7. Implement role-based authorization

### Real-Time Subscriptions

**Prompt:** "Build a tRPC subscription that sends real-time notifications when new messages are posted. Use WebSocket transport."

Claude will:
1. Configure WebSocket link on client
2. Create subscription procedure
3. Implement event emitter pattern
4. Add connection status handling
5. Include automatic reconnection
6. Type subscription payloads properly
7. Add subscription filters

### Full-Stack T3 App

**Prompt:** "Create a complete T3 Stack application with tRPC, Prisma, NextAuth, and Tailwind. Include user authentication, database models, and type-safe API routes."

Claude will:
1. Initialize T3 app with create-t3-app
2. Set up Prisma schema and migrations
3. Configure NextAuth providers
4. Create tRPC routers for all features
5. Build authenticated UI components
6. Add optimistic updates with React Query
7. Include comprehensive error handling

## Tips for Best Results

1. **Use Zod for Validation**: tRPC integrates perfectly with Zod. Always request Zod schemas for input validation to get runtime safety matching TypeScript types.

2. **Leverage Context**: Put database clients, auth sessions, and shared utilities in tRPC context for type-safe access across all procedures.

3. **React Query Integration**: tRPC's React hooks are powered by React Query. Request configurations for caching, refetching, and optimistic updates.

4. **Organize with Sub-Routers**: For large APIs, ask Claude to split procedures into feature-based sub-routers (users, posts, comments) merged into a root router.

5. **Type Inference Magic**: tRPC's `inferProcedureInput` and `inferProcedureOutput` utilities maintain types across client/server. Request these for shared type definitions.

6. **Error Handling**: Use tRPC's `TRPCError` with specific codes (BAD_REQUEST, UNAUTHORIZED, etc.) for consistent error responses.

## Common Workflows

### E-Commerce API
```
"Build a type-safe e-commerce API with tRPC:
1. Product catalog with filtering and search
2. Shopping cart management
3. Order processing with Stripe
4. User authentication with NextAuth
5. Admin dashboard procedures
6. Real-time inventory updates
7. Include Zod validation and Prisma integration"
```

### Social Media Backend
```
"Create a social media backend using tRPC:
1. User profiles with follow/unfollow
2. Posts with likes and comments
3. Real-time notifications via subscriptions
4. Image uploads to S3
5. Feed algorithm with pagination
6. Direct messaging between users
7. Content moderation procedures"
```

### SaaS Multi-Tenant API
```
"Build a multi-tenant SaaS API with tRPC:
1. Organization and team management
2. Role-based access control middleware
3. Usage tracking and billing
4. Webhook integrations
5. Audit logging for all actions
6. Rate limiting per tenant
7. Data isolation at database level"
```

### AI Chat Application
```
"Create a chat app with tRPC and streaming:
1. OpenAI integration with streaming responses
2. Chat history with Prisma
3. Real-time message updates
4. Typing indicators via subscriptions
5. File uploads for context
6. Conversation summarization
7. Cost tracking per user"
```

## Troubleshooting

**Issue:** Type errors between client and server
**Solution:** Ensure both use the same TypeScript version and tRPC version. Export `AppRouter` type from server and import on client. Run `tsc --noEmit` to catch type issues.

**Issue:** Queries not refetching properly
**Solution:** Configure React Query's `staleTime` and `cacheTime`. Use `utils.invalidate()` after mutations or enable optimistic updates with `onMutate`.

**Issue:** Authentication context undefined
**Solution:** Verify middleware runs before protected procedures. Check that `createContext` properly extracts auth token from headers. Ensure client passes credentials.

**Issue:** Slow API responses
**Solution:** Add database query optimization, implement batching with DataLoader pattern, use tRPC's batching link on client, and consider Redis caching for expensive operations.

**Issue:** WebSocket subscriptions disconnecting
**Solution:** Implement heartbeat/ping-pong pattern, add automatic reconnection with exponential backoff, check firewall/proxy timeouts, and use connection pooling.

**Issue:** Zod validation too strict
**Solution:** Use `.optional()`, `.nullable()`, or `.default()` on schema fields. For flexible objects, use `z.record()` or `.passthrough()` to allow extra keys.

## Learn More

- [tRPC Official Documentation](https://trpc.io/docs/)
- [T3 Stack Tutorial](https://create.t3.gg/)
- [tRPC with Next.js 15 Guide](https://trpc.io/docs/nextjs)
- [React Query Integration](https://trpc.io/docs/react-query)
- [tRPC Awesome List](https://github.com/trpc/trpc/blob/main/www/docs/awesome-trpc.md)


## Key Features

- End-to-end type safety without code generation
- Zero runtime dependencies and tiny bundle size
- Automatic React Query hooks generation
- WebSocket subscriptions support

## Use Cases

- Full-stack TypeScript applications
- Real-time collaborative apps
- Type-safe microservices communication

## Examples

### Example 1: tRPC Server Setup

```typescript
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';
import { db } from './db';

// Context creation
export const createContext = async ({ req }: { req: Request }) => {
  const token = req.headers.get('authorization')?.replace('Bearer ', '');
  const user = token ? await verifyToken(token) : null;
  
  return {
    db,
    user,
  };
};

type Context = Awaited<ReturnType<typeof createContext>>;

const t = initTRPC.context<Context>().create();

// Middleware
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: {
      user: ctx.user,
    },
  });
});

// Procedures
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(isAuthed);

// Router
export const appRouter = t.router({
  users: t.router({
    list: publicProcedure
      .query(async ({ ctx }) => {
        return ctx.db.user.findMany();
      }),
    
    create: protectedProcedure
      .input(
        z.object({
          name: z.string().min(3),
          email: z.string().email(),
        })
      )
      .mutation(async ({ ctx, input }) => {
        return ctx.db.user.create({
          data: input,
        });
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

### Example 2: Next.js API Route

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter, createContext } from '~/server/trpc';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  });

export { handler as GET, handler as POST };
```

### Example 3: React Client Usage

```typescript
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { trpc } from '~/utils/trpc';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: 'http://localhost:3000/api/trpc',
          headers() {
            return {
              authorization: `Bearer ${getToken()}`,
            };
          },
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}

// Component usage
export function UsersList() {
  const { data: users, isLoading } = trpc.users.list.useQuery();
  const createUser = trpc.users.create.useMutation();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {users?.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
      <button
        onClick={() =>
          createUser.mutate({
            name: 'New User',
            email: 'user@example.com',
          })
        }
      >
        Add User
      </button>
    </div>
  );
}
```

### Example 4: Real-Time Subscription

```typescript
import { EventEmitter } from 'events';
import { observable } from '@trpc/server/observable';

const ee = new EventEmitter();

export const appRouter = t.router({
  messages: t.router({
    onNew: publicProcedure.subscription(() => {
      return observable<Message>((emit) => {
        const onMessage = (data: Message) => {
          emit.next(data);
        };
        
        ee.on('newMessage', onMessage);
        
        return () => {
          ee.off('newMessage', onMessage);
        };
      });
    }),
    
    send: protectedProcedure
      .input(z.object({ text: z.string() }))
      .mutation(async ({ ctx, input }) => {
        const message = await ctx.db.message.create({
          data: {
            text: input.text,
            userId: ctx.user.id,
          },
        });
        
        ee.emit('newMessage', message);
        return message;
      }),
  }),
});
```

## Troubleshooting

### Type inference not working

Export AppRouter type from server, import on client. Ensure same TypeScript and tRPC versions. Check tsconfig.json has strict: true.

### React Query hooks missing

Verify trpc.Provider wraps app with QueryClientProvider. Check createTRPCReact import and proper initialization.

### CORS errors

Add CORS middleware to tRPC handler or set proper headers in Next.js API route. For development, use proxy in next.config.js.

## Learn More

For additional documentation and resources, visit:

https://trpc.io/docs/
