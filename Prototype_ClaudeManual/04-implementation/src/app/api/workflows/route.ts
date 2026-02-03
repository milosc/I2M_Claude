import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

// Default workflow path (configurable via query param or settings)
// Note: Use correct case for folder name (Workflows, not workflows)
const DEFAULT_WORKFLOW_PATH = '.claude/architecture/Workflows';

// Resolve to project root (go up from 04-implementation to project root)
function getProjectRoot(): string {
  // From 04-implementation, go up to Prototype_ClaudeManual, then up to project root
  return path.resolve(process.cwd(), '..', '..');
}

interface WorkflowFile {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  stage: string;
  children?: WorkflowFile[];
}

interface WorkflowContent {
  id: string;
  name: string;
  path: string;
  content: string;
  stage: string;
}

// Helper to get stage name from folder path
function getStageFromPath(folderName: string): string {
  // Map folder names to stages
  const stageMap: Record<string, string> = {
    'Discovery Phase': 'Discovery',
    'Idea Shaping and Validation Phase': 'Prototype',
    'Solution Specification Phase': 'ProductSpecs',
    'Solution Architecture Phase': 'SolArch',
    'Implementation Phase': 'Implementation',
    'ChangeManagement': 'ChangeManagement',
  };
  return stageMap[folderName] || folderName;
}

// Helper to create display name
function createDisplayName(stage: string, fileName: string): string {
  // Remove .md extension and format nicely
  const baseName = fileName.replace(/\.md$/, '');
  return `${stage} - ${baseName}`;
}

// Recursively scan directory for markdown files
async function scanDirectory(dirPath: string, basePath: string): Promise<WorkflowFile[]> {
  const items: WorkflowFile[] = [];

  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      const relativePath = path.relative(basePath, fullPath);

      if (entry.isDirectory()) {
        const children = await scanDirectory(fullPath, basePath);
        if (children.length > 0) {
          const stage = getStageFromPath(entry.name);
          items.push({
            id: relativePath.replace(/[\/\\]/g, '-'),
            name: entry.name,
            path: relativePath,
            type: 'folder',
            stage,
            children,
          });
        }
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const parentFolder = path.basename(path.dirname(fullPath));
        const stage = getStageFromPath(parentFolder);
        items.push({
          id: relativePath.replace(/[\/\\]/g, '-').replace(/\.md$/, ''),
          name: createDisplayName(stage, entry.name),
          path: relativePath,
          type: 'file',
          stage,
        });
      }
    }
  } catch (error) {
    console.error(`Error scanning directory ${dirPath}:`, error);
  }

  return items;
}

// GET /api/workflows - List all workflows in hierarchy
// GET /api/workflows?file=<path> - Get specific file content
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const fileParam = searchParams.get('file');
  const customPath = searchParams.get('workflowPath');

  // Resolve workflow path (use custom path or default)
  const workflowPath = customPath || DEFAULT_WORKFLOW_PATH;
  const projectRoot = getProjectRoot();
  const absolutePath = path.resolve(projectRoot, workflowPath);

  // If file parameter is provided, return file content
  if (fileParam) {
    try {
      const filePath = path.join(absolutePath, fileParam);

      // Security check: ensure path is within workflow directory
      const normalizedFilePath = path.normalize(filePath);
      if (!normalizedFilePath.startsWith(absolutePath)) {
        return NextResponse.json({ error: 'Invalid file path' }, { status: 400 });
      }

      const content = await fs.readFile(filePath, 'utf-8');
      const parentFolder = path.basename(path.dirname(filePath));
      const stage = getStageFromPath(parentFolder);

      const result: WorkflowContent = {
        id: fileParam.replace(/[\/\\]/g, '-').replace(/\.md$/, ''),
        name: createDisplayName(stage, path.basename(fileParam)),
        path: fileParam,
        content,
        stage,
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
      workflowPath,
      defaultPath: DEFAULT_WORKFLOW_PATH,
      items: hierarchy,
    });
  } catch (error) {
    console.error('Error scanning workflows:', error);
    return NextResponse.json({
      error: 'Failed to scan workflow directory',
      workflowPath,
    }, { status: 500 });
  }
}
