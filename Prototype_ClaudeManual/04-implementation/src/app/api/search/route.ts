import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface SearchableItem {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
  type: string;
}

function parseYamlFrontmatter(content: string): Record<string, string> {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) return {};

  const frontmatter: Record<string, string> = {};
  const lines = frontmatterMatch[1].split('\n');
  let currentKey = '';
  let currentValue = '';

  for (const line of lines) {
    const keyMatch = line.match(/^(\w[\w-]*):(.*)$/);
    if (keyMatch && !line.trim().endsWith(':')) {
      if (currentKey) {
        frontmatter[currentKey] = currentValue.trim();
      }
      currentKey = keyMatch[1];
      currentValue = keyMatch[2].trim();
    } else if (keyMatch && line.trim().endsWith(':')) {
      if (currentKey) {
        frontmatter[currentKey] = currentValue.trim();
      }
      currentKey = '';
      currentValue = '';
    } else if (currentKey && line.startsWith('  ') && !line.includes('- ')) {
      currentValue += ' ' + line.trim();
    }
  }
  if (currentKey) {
    frontmatter[currentKey] = currentValue.trim();
  }

  return frontmatter;
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
        items.push({
          id: entry.name,
          name: frontmatter.name ? formatName(frontmatter.name) : formatName(entry.name),
          description: (frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(entry.name, 'skill'),
          path: `.claude/skills/${entry.name}/SKILL.md`,
          type: 'Skill'
        });
      } catch (err) {
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
        items.push({
          id: commandId,
          name: frontmatter.name ? formatName(frontmatter.name) : formatName(commandId),
          description: (frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(commandId, 'command'),
          path: `.claude/commands/${file}`,
          type: 'Command'
        });
      } catch (err) {
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
        items.push({
          id: agentId,
          name: frontmatter.name ? formatName(frontmatter.name) : formatName(agentId),
          description: (frontmatter.description || '').replace(/^["']|["']$/g, ''),
          stage: determineStage(agentId, 'agent'),
          path: `.claude/agents/${file}`,
          type: 'Agent'
        });
      } catch (err) {
        // Skip invalid files
      }
    }
  }

  return items;
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q')?.toLowerCase() || '';

  if (!query) {
    return NextResponse.json([]);
  }

  try {
    const allItems = loadAllItems();

    // Search: match query in name, description, or stage
    const results = allItems
      .filter((item) => {
        const matchName = item.name.toLowerCase().includes(query);
        const matchDescription = item.description.toLowerCase().includes(query);
        const matchStage = item.stage.toLowerCase().includes(query);
        const matchId = item.id.toLowerCase().includes(query);
        return matchName || matchDescription || matchStage || matchId;
      })
      .map((item) => {
        // Calculate relevance score
        let score = 0;
        if (item.name.toLowerCase().includes(query)) score += 10;
        if (item.id.toLowerCase().includes(query)) score += 8;
        if (item.description.toLowerCase().includes(query)) score += 5;
        if (item.stage.toLowerCase().includes(query)) score += 2;
        return { ...item, score };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 50) // Limit results
      .map(({ score, ...item }) => item);

    return NextResponse.json(results);
  } catch (error) {
    console.error('Search error:', error);
    return NextResponse.json([]);
  }
}
