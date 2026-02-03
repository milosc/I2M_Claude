import { NextRequest, NextResponse } from 'next/server';

// Mock preferences storage (in real app, would use database)
let mockPreferences = {
  theme: 'system',
  fontSize: 'medium',
  favorites: [] as string[],
  recentlyViewed: [] as string[],
};

export async function GET() {
  return NextResponse.json(mockPreferences);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Update preferences
  mockPreferences = { ...mockPreferences, ...body };

  return NextResponse.json(mockPreferences);
}

export async function PUT(request: NextRequest) {
  const body = await request.json();

  // Replace entire preferences object
  mockPreferences = body;

  return NextResponse.json(mockPreferences);
}
