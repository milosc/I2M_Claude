import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface CommandContent {
  purpose: string;
  example: string;
  workflow: string;
}

interface FrontmatterAttributes {
  model?: string | null;
  argument_hint?: string | null;
  allowed_tools?: string[];
  invokes_skills?: string[];
  orchestrates_agents?: string[];
  [key: string]: unknown;
}

interface Command {
  id: string;
  name: string;
  type: 'command';
  description: string;
  stage: string;
  path: string;
  model: string | null;
  allowed_tools: string[];
  argument_hint: string | null;
  invokes_skills: string[];
  orchestrates_agents: string[];
  frontmatter: FrontmatterAttributes;
  rawContent: string;
  content: CommandContent;
}

function parseYamlFrontmatter(content: string): { frontmatter: Record<string, string>; body: string } {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!frontmatterMatch) return { frontmatter: {}, body: content };

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

  return { frontmatter, body: frontmatterMatch[2] || '' };
}

function extractSection(body: string, sectionName: string): string {
  const patterns = [
    new RegExp(`##\\s*${sectionName}[\\s\\S]*?(?=\\n##|$)`, 'i'),
    new RegExp(`###\\s*${sectionName}[\\s\\S]*?(?=\\n###|\\n##|$)`, 'i'),
  ];

  for (const pattern of patterns) {
    const match = body.match(pattern);
    if (match) {
      return match[0].replace(/^##?\s*[^\n]+\n/, '').trim();
    }
  }
  return '';
}

function extractPurpose(body: string, description: string): string {
  const titleMatch = body.match(/^#\s+[^\n]+\n\n([^\n#]+)/);
  if (titleMatch) {
    return titleMatch[1].trim();
  }
  return description;
}

function extractUsage(body: string): string {
  const usageSection = extractSection(body, 'Usage|Synopsis|How to Use|Quick Start');
  if (usageSection) {
    return usageSection.substring(0, 500);
  }
  return '';
}

function extractWorkflow(body: string): string {
  const workflowSection = extractSection(body, 'Workflow|Execution|Process|Steps|Phases');
  if (workflowSection) {
    return workflowSection.substring(0, 500);
  }
  return '';
}

function determineStage(filename: string): string {
  const name = filename.toLowerCase();
  if (name.startsWith('discovery')) return 'Discovery';
  if (name.startsWith('prototype')) return 'Prototype';
  if (name.startsWith('productspecs')) return 'ProductSpecs';
  if (name.startsWith('solarch')) return 'SolArch';
  if (name.startsWith('htec-sdd') || name.startsWith('implementation')) return 'Implementation';
  if (name.startsWith('grc')) return 'GRC';
  if (name.startsWith('security')) return 'Security';
  if (name.startsWith('kaizen')) return 'Kaizen';
  if (name.startsWith('rules')) return 'Rules';
  if (name.startsWith('trace') || name.startsWith('traceability')) return 'Traceability';
  return 'Utility';
}

function parseAllowedTools(value: string | undefined): string[] {
  if (!value) return [];
  return value.split(',').map(t => t.trim()).filter(Boolean);
}

function formatCommandName(filename: string): string {
  return filename
    .replace(/-/g, ' ')
    .replace(/_/g, ' ')
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

export async function GET() {
  try {
    // Navigate to project root (.claude folder is at project root)
    // 04-implementation -> Prototype_ClaudeManual -> claudeManual (2 levels up)
    const projectRoot = path.resolve(process.cwd(), '../..');
    const commandsDir = path.join(projectRoot, '.claude', 'commands');

    if (!fs.existsSync(commandsDir)) {
      console.error('Commands directory not found:', commandsDir);
      return NextResponse.json([]);
    }

    const commands: Command[] = [];
    const files = fs.readdirSync(commandsDir);

    for (const file of files) {
      if (!file.endsWith('.md')) continue;

      // Skip reference files and backup files
      if (file.includes('REFERENCE') || file.endsWith('.bak')) continue;

      const commandPath = path.join(commandsDir, file);
      const stat = fs.statSync(commandPath);
      if (!stat.isFile()) continue;

      try {
        const fileContent = fs.readFileSync(commandPath, 'utf-8');
        const { frontmatter, body } = parseYamlFrontmatter(fileContent);

        const commandId = file.replace('.md', '');
        const description = (frontmatter.description || '').replace(/^["']|["']$/g, '');

        // Skip files without proper frontmatter
        if (!frontmatter.description && !frontmatter.name) continue;

        // Extract content from body
        const purpose = extractPurpose(body, description);
        const usage = extractUsage(body);
        const workflow = extractWorkflow(body);

        // Build example from argument_hint
        const argHint = frontmatter['argument-hint'] || '';
        const example = argHint
          ? `/${commandId} ${argHint}`
          : `/${commandId}`;

        commands.push({
          id: commandId,
          name: frontmatter.name ? formatCommandName(frontmatter.name) : formatCommandName(commandId),
          type: 'command',
          description: description,
          stage: determineStage(commandId),
          path: `.claude/commands/${file}`,
          model: frontmatter.model || null,
          allowed_tools: parseAllowedTools(frontmatter['allowed-tools']),
          argument_hint: frontmatter['argument-hint'] || null,
          invokes_skills: [],
          orchestrates_agents: [],
          frontmatter: {
            model: frontmatter.model || null,
            argument_hint: frontmatter['argument-hint'] || null,
            allowed_tools: parseAllowedTools(frontmatter['allowed-tools']),
            invokes_skills: [],
            orchestrates_agents: [],
          },
          rawContent: body,
          content: {
            purpose: purpose || description,
            example: example,
            workflow: workflow || usage || 'See command documentation for details'
          }
        });
      } catch (err) {
        console.error(`Error parsing command ${file}:`, err);
      }
    }

    // Sort by stage then name
    commands.sort((a, b) => {
      const stageOrder = ['Discovery', 'Prototype', 'ProductSpecs', 'SolArch', 'Implementation', 'GRC', 'Security', 'Traceability', 'Kaizen', 'Rules', 'Utility'];
      const stageCompare = stageOrder.indexOf(a.stage) - stageOrder.indexOf(b.stage);
      if (stageCompare !== 0) return stageCompare;
      return a.name.localeCompare(b.name);
    });

    return NextResponse.json(commands);
  } catch (error) {
    console.error('Error loading commands:', error);
    return NextResponse.json([]);
  }
}
