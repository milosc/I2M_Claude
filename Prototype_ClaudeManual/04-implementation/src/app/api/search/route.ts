import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export interface SearchableItem {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Hook' | 'Workflow' | 'Architecture';
  tags?: string[];
  content?: string;
}

interface ParsedFrontmatter {
  name?: string;
  description?: string;
  tags?: string[];
  [key: string]: string | string[] | undefined;
}

function parseYamlFrontmatter(content: string): ParsedFrontmatter {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) return {};

  const frontmatter: ParsedFrontmatter = {};
  const lines = frontmatterMatch[1].split('\n');
  let currentKey = '';
  let currentValue = '';
  let inArray = false;
  let arrayValues: string[] = [];

  for (const line of lines) {
    // Check for array item
    if (inArray && line.match(/^\s+-\s+(.+)$/)) {
      const match = line.match(/^\s+-\s+(.+)$/);
      if (match) {
        arrayValues.push(match[1].replace(/^["']|["']$/g, '').trim());
      }
      continue;
    }

    // Check for new key
    const keyMatch = line.match(/^(\w[\w-]*):(.*)$/);
    if (keyMatch) {
      // Save previous key
      if (currentKey) {
        if (inArray) {
          frontmatter[currentKey] = arrayValues;
        } else {
          frontmatter[currentKey] = currentValue.trim();
        }
      }

      currentKey = keyMatch[1];
      const value = keyMatch[2].trim();

      // Check if this starts an array
      if (value === '' || value === '[]') {
        inArray = true;
        arrayValues = [];
        currentValue = '';
      } else {
        inArray = false;
        currentValue = value;
      }
    } else if (currentKey && line.startsWith('  ') && !inArray) {
      currentValue += ' ' + line.trim();
    }
  }

  // Save last key
  if (currentKey) {
    if (inArray) {
      frontmatter[currentKey] = arrayValues;
    } else {
      frontmatter[currentKey] = currentValue.trim();
    }
  }

  return frontmatter;
}

function getContentBody(content: string): string {
  // Remove frontmatter and get body content
  const withoutFrontmatter = content.replace(/^---\n[\s\S]*?\n---\n?/, '');
  // Truncate to first 500 chars for search preview
  return withoutFrontmatter.slice(0, 500).trim();
}

function determineStage(name: string, type: string): string {
  const lowerName = name.toLowerCase();
  if (lowerName.startsWith('discovery')) return 'Discovery';
  if (lowerName.startsWith('prototype')) return 'Prototype';
  if (lowerName.startsWith('productspecs')) return 'ProductSpecs';
  if (lowerName.startsWith('solarch') || lowerName.startsWith('solutionarchitecture')) return 'SolArch';
  if (lowerName.startsWith('htec-sdd') || lowerName.startsWith('implementation') || lowerName.startsWith('planning')) return 'Implementation';
  if (lowerName.startsWith('quality')) return 'Quality';
  if (lowerName.startsWith('grc') || lowerName.startsWith('compliance') || lowerName.startsWith('privacy') || lowerName.startsWith('security')) return 'GRC';
  if (lowerName.startsWith('process-integrity')) return 'Process';
  if (lowerName.startsWith('reflexion')) return 'Reflexion';
  if (lowerName.startsWith('trace') || lowerName.startsWith('traceability')) return 'Traceability';
  if (lowerName.startsWith('kaizen')) return 'Kaizen';
  if (lowerName.startsWith('rules')) return 'Rules';
  return 'Utility';
}

function formatName(filename: string): string {
  return filename
    .replace(/-/g, ' ')
    .replace(/_/g, ' ')
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

function scanDirectoryRecursive(dir: string, extension: string): string[] {
  const results: string[] = [];
  if (!fs.existsSync(dir)) return results;

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...scanDirectoryRecursive(fullPath, extension));
    } else if (entry.isFile() && entry.name.endsWith(extension)) {
      results.push(fullPath);
    }
  }
  return results;
}

function loadAllItems(): SearchableItem[] {
  // 04-implementation -> Prototype_ClaudeManual -> claudeManual (2 levels up)
  const projectRoot = path.resolve(process.cwd(), '../..');
  const items: SearchableItem[] = [];

  // Load skills
  const skillsDir = path.join(projectRoot, '.claude', 'skills');
  if (fs.existsSync(skillsDir)) {
    const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const skillMdPath = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillMdPath)) continue;
      try {
        const content = fs.readFileSync(skillMdPath, 'utf-8');
        const frontmatter = parseYamlFrontmatter(content);
        if (!frontmatter.description && !frontmatter.name) continue;
        const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
        items.push({
          id: entry.name,
          name: frontmatter.name ? formatName(String(frontmatter.name)) : formatName(entry.name),
          description: String(frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(entry.name, 'skill'),
          path: `.claude/skills/${entry.name}/SKILL.md`,
          type: 'Skill',
          tags,
          content: getContentBody(content)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  // Load commands
  const commandsDir = path.join(projectRoot, '.claude', 'commands');
  if (fs.existsSync(commandsDir)) {
    const files = fs.readdirSync(commandsDir);
    for (const file of files) {
      if (!file.endsWith('.md') || file.includes('REFERENCE') || file.endsWith('.bak')) continue;
      const commandPath = path.join(commandsDir, file);
      try {
        const stat = fs.statSync(commandPath);
        if (!stat.isFile()) continue;
        const content = fs.readFileSync(commandPath, 'utf-8');
        const frontmatter = parseYamlFrontmatter(content);
        if (!frontmatter.description && !frontmatter.name) continue;
        const commandId = file.replace('.md', '');
        const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
        items.push({
          id: commandId,
          name: frontmatter.name ? formatName(String(frontmatter.name)) : formatName(commandId),
          description: String(frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(commandId, 'command'),
          path: `.claude/commands/${file}`,
          type: 'Command',
          tags,
          content: getContentBody(content)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  // Load agents
  const agentsDir = path.join(projectRoot, '.claude', 'agents');
  if (fs.existsSync(agentsDir)) {
    const files = fs.readdirSync(agentsDir);
    for (const file of files) {
      if (!file.endsWith('.md') || file === 'README.md' || file.includes('REGISTRY')) continue;
      const agentPath = path.join(agentsDir, file);
      try {
        const stat = fs.statSync(agentPath);
        if (!stat.isFile()) continue;
        const content = fs.readFileSync(agentPath, 'utf-8');
        const frontmatter = parseYamlFrontmatter(content);
        if (!frontmatter.description && !frontmatter.name) continue;
        const agentId = file.replace('.md', '');
        const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
        items.push({
          id: agentId,
          name: frontmatter.name ? formatName(String(frontmatter.name)) : formatName(agentId),
          description: String(frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(agentId, 'agent'),
          path: `.claude/agents/${file}`,
          type: 'Agent',
          tags,
          content: getContentBody(content)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  // Load hooks
  const hooksDir = path.join(projectRoot, '.claude', 'hooks');
  if (fs.existsSync(hooksDir)) {
    const files = fs.readdirSync(hooksDir);
    for (const file of files) {
      if (!file.endsWith('.py')) continue;
      const hookPath = path.join(hooksDir, file);
      try {
        const stat = fs.statSync(hookPath);
        if (!stat.isFile()) continue;
        const content = fs.readFileSync(hookPath, 'utf-8');
        // Extract docstring or first comment
        let description = '';
        const docstringMatch = content.match(/^"""([\s\S]*?)"""/m) || content.match(/^'''([\s\S]*?)'''/m);
        if (docstringMatch) {
          description = docstringMatch[1].trim().split('\n')[0];
        } else {
          const commentMatch = content.match(/^#\s*(.+)$/m);
          if (commentMatch) {
            description = commentMatch[1].trim();
          }
        }
        const hookId = file.replace('.py', '');
        items.push({
          id: hookId,
          name: formatName(hookId),
          description: description || `Python hook: ${hookId}`,
          stage: determineStage(hookId, 'hook'),
          path: `.claude/hooks/${file}`,
          type: 'Hook',
          tags: [],
          content: content.slice(0, 500)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  // Load workflows
  const workflowsDir = path.join(projectRoot, '.claude', 'architecture', 'Workflows');
  if (fs.existsSync(workflowsDir)) {
    const workflowFiles = scanDirectoryRecursive(workflowsDir, '.md');
    for (const filePath of workflowFiles) {
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const frontmatter = parseYamlFrontmatter(content);
        const relativePath = path.relative(projectRoot, filePath);
        const fileName = path.basename(filePath, '.md');
        const parentDir = path.basename(path.dirname(filePath));
        const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
        items.push({
          id: `workflow-${fileName}`,
          name: frontmatter.name ? formatName(String(frontmatter.name)) : formatName(fileName),
          description: String(frontmatter.description || `Workflow: ${fileName}`).replace(/^["']|["']$/g, ''),
          stage: determineStage(parentDir, 'workflow'),
          path: relativePath.replace(/\\/g, '/'),
          type: 'Workflow',
          tags,
          content: getContentBody(content)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  // Load architecture docs (excluding Workflows)
  const archDir = path.join(projectRoot, '.claude', 'architecture');
  if (fs.existsSync(archDir)) {
    const archFiles = scanDirectoryRecursive(archDir, '.md');
    for (const filePath of archFiles) {
      // Skip workflow files
      if (filePath.includes('Workflows')) continue;
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const frontmatter = parseYamlFrontmatter(content);
        const relativePath = path.relative(projectRoot, filePath);
        const fileName = path.basename(filePath, '.md');
        const parentDir = path.basename(path.dirname(filePath));
        const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
        items.push({
          id: `arch-${fileName}`,
          name: frontmatter.name ? formatName(String(frontmatter.name)) : formatName(fileName),
          description: String(frontmatter.description || `Architecture doc: ${fileName}`).replace(/^["']|["']$/g, ''),
          stage: parentDir === 'architecture' ? 'Utility' : determineStage(parentDir, 'architecture'),
          path: relativePath.replace(/\\/g, '/'),
          type: 'Architecture',
          tags,
          content: getContentBody(content)
        });
      } catch {
        // Skip invalid files
      }
    }
  }

  return items;
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q')?.toLowerCase() || '';
  const typeFilter = searchParams.get('type'); // Optional type filter

  if (!query) {
    return NextResponse.json([]);
  }

  try {
    let allItems = loadAllItems();

    // Apply type filter if provided
    if (typeFilter) {
      const types = typeFilter.split(',');
      allItems = allItems.filter(item => types.includes(item.type));
    }

    // Search: match query in name, description, stage, content, or tags
    const results = allItems
      .filter((item) => {
        const matchName = item.name.toLowerCase().includes(query);
        const matchDescription = item.description.toLowerCase().includes(query);
        const matchStage = item.stage.toLowerCase().includes(query);
        const matchId = item.id.toLowerCase().includes(query);
        const matchContent = item.content?.toLowerCase().includes(query) || false;
        const matchTags = item.tags?.some(tag => tag.toLowerCase().includes(query)) || false;
        return matchName || matchDescription || matchStage || matchId || matchContent || matchTags;
      })
      .map((item) => {
        // Calculate relevance score
        let score = 0;
        if (item.name.toLowerCase().includes(query)) score += 10;
        if (item.id.toLowerCase().includes(query)) score += 8;
        if (item.description.toLowerCase().includes(query)) score += 5;
        if (item.tags?.some(tag => tag.toLowerCase().includes(query))) score += 4;
        if (item.content?.toLowerCase().includes(query)) score += 3;
        if (item.stage.toLowerCase().includes(query)) score += 2;
        return { ...item, score };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 100) // Limit results
      .map(({ score, ...item }) => item);

    return NextResponse.json(results);
  } catch (error) {
    console.error('Search error:', error);
    return NextResponse.json([]);
  }
}
