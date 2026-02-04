import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

// Default architecture path
const DEFAULT_ARCHITECTURE_PATH = '.claude/architecture';

// Resolve to project root (go up from 04-implementation to project root)
function getProjectRoot(): string {
  // From 04-implementation, go up to Prototype_ClaudeManual, then up to project root
  return path.resolve(process.cwd(), '..', '..');
}

interface ArchitectureFile {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  category: string;
  children?: ArchitectureFile[];
}

interface ArchitectureContent {
  id: string;
  name: string;
  path: string;
  content: string;
  category: string;
}

// Helper to get category name from folder path
function getCategoryFromPath(folderName: string): string {
  // Map folder names to categories
  const categoryMap: Record<string, string> = {
    'CC': 'Claude Code',
    'Workflows': 'Workflows',
    'hooks': 'Hooks',
    'LSP Integrations': 'LSP',
    'Memory Management and Traceability': 'Traceability',
    'to be solved': 'To Be Solved',
  };
  return categoryMap[folderName] || folderName;
}

// Helper to create display name
function createDisplayName(fileName: string): string {
  // Remove .md extension and format nicely
  return fileName.replace(/\.md$/, '');
}

// Recursively scan directory for markdown files
async function scanDirectory(dirPath: string, basePath: string): Promise<ArchitectureFile[]> {
  const items: ArchitectureFile[] = [];

  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      const relativePath = path.relative(basePath, fullPath);

      if (entry.isDirectory()) {
        const children = await scanDirectory(fullPath, basePath);
        // Include folders even if empty (they might contain non-md files)
        const category = getCategoryFromPath(entry.name);
        items.push({
          id: relativePath.replace(/[\/\\]/g, '-'),
          name: entry.name,
          path: relativePath,
          type: 'folder',
          category,
          children,
        });
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const parentFolder = path.basename(path.dirname(fullPath));
        const category = getCategoryFromPath(parentFolder);
        items.push({
          id: relativePath.replace(/[\/\\]/g, '-').replace(/\.md$/, ''),
          name: createDisplayName(entry.name),
          path: relativePath,
          type: 'file',
          category,
        });
      }
    }
  } catch (error) {
    console.error(`Error scanning directory ${dirPath}:`, error);
  }

  return items;
}

// GET /api/architecture - List all architecture docs in hierarchy
// GET /api/architecture?file=<path> - Get specific file content
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const fileParam = searchParams.get('file');
  const customPath = searchParams.get('architecturePath');

  // Resolve architecture path (use custom path or default)
  const architecturePath = customPath || DEFAULT_ARCHITECTURE_PATH;
  const projectRoot = getProjectRoot();
  const absolutePath = path.resolve(projectRoot, architecturePath);

  // If file parameter is provided, return file content
  if (fileParam) {
    try {
      const filePath = path.join(absolutePath, fileParam);

      // Security check: ensure path is within architecture directory
      const normalizedFilePath = path.normalize(filePath);
      if (!normalizedFilePath.startsWith(absolutePath)) {
        return NextResponse.json({ error: 'Invalid file path' }, { status: 400 });
      }

      const content = await fs.readFile(filePath, 'utf-8');
      const parentFolder = path.basename(path.dirname(filePath));
      const category = getCategoryFromPath(parentFolder);

      const result: ArchitectureContent = {
        id: fileParam.replace(/[\/\\]/g, '-').replace(/\.md$/, ''),
        name: createDisplayName(path.basename(fileParam)),
        path: fileParam,
        content,
        category,
      };

      return NextResponse.json(result);
    } catch (error) {
      console.error('Error reading file:', error);
      return NextResponse.json({ error: 'File not found' }, { status: 404 });
    }
  }

  // Return hierarchical structure
  try {
    const hierarchy = await scanDirectory(absolutePath, absolutePath);

    return NextResponse.json({
      architecturePath,
      defaultPath: DEFAULT_ARCHITECTURE_PATH,
      items: hierarchy,
    });
  } catch (error) {
    console.error('Error scanning architecture:', error);
    return NextResponse.json({
      error: 'Failed to scan architecture directory',
      architecturePath,
    }, { status: 500 });
  }
}
