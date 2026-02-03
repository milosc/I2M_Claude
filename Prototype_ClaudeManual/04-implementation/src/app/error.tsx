'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
      <div className="max-w-md text-center space-y-4">
        <h1 className="text-2xl font-bold text-red-500">Something went wrong</h1>
        <p className="text-secondary">{error.message}</p>
        <div className="flex gap-2 justify-center">
          <button
            onClick={reset}
            className="px-4 py-2 bg-accent-default text-white rounded hover:bg-accent-hover"
          >
            Try again
          </button>
          <button
            onClick={() => (window.location.href = '/')}
            className="px-4 py-2 border border-border rounded hover:bg-surface-2"
          >
            Go to Home
          </button>
        </div>
      </div>
    </div>
  );
}
