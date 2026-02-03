export default function Loading() {
  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
      <div className="text-center space-y-4">
        <div className="w-16 h-16 border-4 border-accent-default border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-secondary">Loading...</p>
      </div>
    </div>
  );
}
