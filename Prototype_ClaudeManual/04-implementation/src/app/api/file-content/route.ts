import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Allowed directories for security
const ALLOWED_DIRS = ['.claude/skills', '.claude/commands', '.claude/agents', '.claude/hooks', '.claude/architecture'];

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const filePath = searchParams.get('path');

  if (!filePath) {
    return NextResponse.json({ error: 'Missing path parameter' }, { status: 400 });
  }

  // Security: Validate path is within allowed directories
  const normalizedPath = path.normalize(filePath).replace(/\\/g, '/');

  // Check for path traversal attempts
  if (normalizedPath.includes('..') || normalizedPath.startsWith('/')) {
    return NextResponse.json({ error: 'Invalid path' }, { status: 400 });
  }

  // Check if path starts with an allowed directory
  const isAllowed = ALLOWED_DIRS.some(dir => normalizedPath.startsWith(dir));
  if (!isAllowed) {
    return NextResponse.json({ error: 'Access denied' }, { status: 403 });
  }

  try {
    // 04-implementation -> Prototype_ClaudeManual -> claudeManual (2 levels up)
    const projectRoot = path.resolve(process.cwd(), '../..');
    const absolutePath = path.join(projectRoot, normalizedPath);

    // Double-check the resolved path is within project root
    const resolvedPath = path.resolve(absolutePath);
    const resolvedProjectRoot = path.resolve(projectRoot);
    if (!resolvedPath.startsWith(resolvedProjectRoot)) {
      return NextResponse.json({ error: 'Access denied' }, { status: 403 });
    }

    // Check if file exists
    if (!fs.existsSync(absolutePath)) {
      return NextResponse.json({ error: 'File not found' }, { status: 404 });
    }

    // Check if it's a file (not directory)
    const stat = fs.statSync(absolutePath);
    if (!stat.isFile()) {
      return NextResponse.json({ error: 'Not a file' }, { status: 400 });
    }

    // Read and return file content
    const content = fs.readFileSync(absolutePath, 'utf-8');
    const fileName = path.basename(absolutePath);
    const fileExtension = path.extname(absolutePath).slice(1);

    return NextResponse.json({
      path: normalizedPath,
      fileName,
      extension: fileExtension,
      content,
      size: stat.size,
      modifiedAt: stat.mtime.toISOString()
    });
  } catch (error) {
    console.error('File content error:', error);
    return NextResponse.json({ error: 'Failed to read file' }, { status: 500 });
  }
}
