import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface AgentContent {
  purpose: string;
  example: string;
  workflow: string;
}

interface HookEntry {
  type: string;
  command: string;
}

interface HookMatcher {
  matcher?: string;
  once?: boolean;
  hooks: HookEntry[];
}

interface ParsedHooks {
  [key: string]: HookMatcher[] | undefined;
}

interface FrontmatterAttributes {
  model?: string | null;
  checkpoint?: number | null;
  color?: string;
  loads_skills?: string[];
  spawned_by?: string[];
  hooks?: ParsedHooks;
  [key: string]: unknown;
}

interface Agent {
  id: string;
  name: string;
  type: 'agent';
  description: string;
  model: string | null;
  checkpoint: number | null;
  path: string;
  tools: string[];
  color: string;
  stage: string;
  loads_skills: string[];
  spawned_by: string[];
  frontmatter: FrontmatterAttributes;
  rawContent: string;
  content: AgentContent;
}

function parseHooksSection(frontmatterText: string): ParsedHooks | undefined {
  const hooksMatch = frontmatterText.match(/^hooks:\s*$/m);
  if (!hooksMatch) return undefined;

  const startIdx = hooksMatch.index! + hooksMatch[0].length;
  const lines = frontmatterText.substring(startIdx).split('\n');

  const hooks: ParsedHooks = {};
  let currentHookType: string | null = null;
  let currentMatcher: HookMatcher | null = null;
  let currentHookEntry: Partial<HookEntry> | null = null;
  let commandLines: string[] = [];

  for (const line of lines) {
    if (line && !line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      break;
    }

    const trimmed = line.trim();
    const indent = line.search(/\S/);

    if (indent === 2 && trimmed.endsWith(':') && !trimmed.startsWith('-')) {
      if (currentHookEntry && currentHookEntry.type && currentMatcher) {
        if (commandLines.length > 0) {
          currentHookEntry.command = commandLines.join(' ').trim();
          commandLines = [];
        }
        currentMatcher.hooks.push(currentHookEntry as HookEntry);
        currentHookEntry = null;
      }
      if (currentMatcher && currentHookType) {
        if (!hooks[currentHookType]) hooks[currentHookType] = [];
        hooks[currentHookType]!.push(currentMatcher);
        currentMatcher = null;
      }
      currentHookType = trimmed.slice(0, -1);
      continue;
    }

    if (trimmed.startsWith('- ') && currentHookType) {
      if (currentHookEntry && currentHookEntry.type && currentMatcher) {
        if (commandLines.length > 0) {
          currentHookEntry.command = commandLines.join(' ').trim();
          commandLines = [];
        }
        currentMatcher.hooks.push(currentHookEntry as HookEntry);
        currentHookEntry = null;
      }
      if (trimmed.startsWith('- matcher:') || trimmed.startsWith('- hooks:')) {
        if (currentMatcher) {
          if (!hooks[currentHookType]) hooks[currentHookType] = [];
          hooks[currentHookType]!.push(currentMatcher);
        }
        currentMatcher = { hooks: [] };
      }

      const content = trimmed.substring(2);
      if (content.startsWith('matcher:')) {
        const matcherValue = content.substring(8).trim().replace(/^["']|["']$/g, '');
        if (currentMatcher) currentMatcher.matcher = matcherValue;
      } else if (content.startsWith('type:')) {
        currentHookEntry = { type: content.substring(5).trim() };
      }
      continue;
    }

    if (currentMatcher && indent >= 6) {
      if (trimmed.startsWith('once:')) {
        currentMatcher.once = trimmed.substring(5).trim() === 'true';
      } else if (trimmed === 'hooks:') {
        // hooks array start
      } else if (trimmed.startsWith('- type:')) {
        if (currentHookEntry && currentHookEntry.type) {
          if (commandLines.length > 0) {
            currentHookEntry.command = commandLines.join(' ').trim();
            commandLines = [];
          }
          currentMatcher.hooks.push(currentHookEntry as HookEntry);
        }
        currentHookEntry = { type: trimmed.substring(7).trim() };
      } else if (trimmed.startsWith('command:')) {
        if (currentHookEntry) {
          const cmdValue = trimmed.substring(8).trim();
          if (cmdValue.startsWith('>-') || cmdValue.startsWith('>')) {
            commandLines = [];
          } else {
            currentHookEntry.command = cmdValue.replace(/^["']|["']$/g, '');
          }
        }
      } else if (currentHookEntry && !trimmed.startsWith('-') && !trimmed.includes(':')) {
        commandLines.push(trimmed);
      }
    }
  }

  if (currentHookEntry && currentHookEntry.type && currentMatcher) {
    if (commandLines.length > 0) {
      currentHookEntry.command = commandLines.join(' ').trim();
    }
    currentMatcher.hooks.push(currentHookEntry as HookEntry);
  }
  if (currentMatcher && currentHookType) {
    if (!hooks[currentHookType]) hooks[currentHookType] = [];
    hooks[currentHookType]!.push(currentMatcher);
  }

  return Object.keys(hooks).length > 0 ? hooks : undefined;
}

function parseYamlFrontmatter(content: string): { frontmatter: Record<string, string>; body: string; hooks: ParsedHooks | undefined } {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!frontmatterMatch) return { frontmatter: {}, body: content, hooks: undefined };

  const frontmatterText = frontmatterMatch[1];
  const frontmatter: Record<string, string> = {};
  const lines = frontmatterText.split('\n');
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

  const hooks = parseHooksSection(frontmatterText);

  return { frontmatter, body: frontmatterMatch[2] || '', hooks };
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

function extractCapabilities(body: string): string[] {
  const section = extractSection(body, 'Capabilities|Features|What It Does|Responsibilities');
  if (!section) return [];

  const bullets = section.match(/^[-*]\s+(.+)$/gm);
  if (bullets) {
    return bullets.map(b => b.replace(/^[-*]\s+/, '').trim());
  }
  return [];
}

function extractWorkflow(body: string): string {
  const workflowSection = extractSection(body, 'Workflow|Execution|Process|How It Works');
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
  if (name.startsWith('implementation') || name.startsWith('planning')) return 'Implementation';
  if (name.startsWith('quality')) return 'Quality';
  if (name.startsWith('compliance') || name.startsWith('privacy') || name.startsWith('security')) return 'GRC';
  if (name.startsWith('process-integrity')) return 'Process';
  if (name.startsWith('reflexion')) return 'Reflexion';
  if (name.startsWith('trace')) return 'Traceability';
  return 'Utility';
}

function determineColor(stage: string): string {
  const colorMap: Record<string, string> = {
    'Discovery': 'blue',
    'Prototype': 'green',
    'ProductSpecs': 'purple',
    'SolArch': 'indigo',
    'Implementation': 'purple',
    'Quality': 'orange',
    'GRC': 'red',
    'Process': 'yellow',
    'Reflexion': 'pink',
    'Traceability': 'teal',
    'Utility': 'gray'
  };
  return colorMap[stage] || 'gray';
}

function parseTools(value: string | undefined): string[] {
  if (!value) return [];
  return value.split(',').map(t => t.trim()).filter(Boolean);
}

function formatAgentName(filename: string): string {
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
    const agentsDir = path.join(projectRoot, '.claude', 'agents');

    if (!fs.existsSync(agentsDir)) {
      console.error('Agents directory not found:', agentsDir);
      return NextResponse.json([]);
    }

    const agents: Agent[] = [];
    const files = fs.readdirSync(agentsDir);

    for (const file of files) {
      if (!file.endsWith('.md')) continue;

      // Skip README and registry files
      if (file === 'README.md' || file.includes('REGISTRY')) continue;

      const agentPath = path.join(agentsDir, file);
      const stat = fs.statSync(agentPath);
      if (!stat.isFile()) continue;

      try {
        const fileContent = fs.readFileSync(agentPath, 'utf-8');
        const { frontmatter, body, hooks } = parseYamlFrontmatter(fileContent);

        const agentId = file.replace('.md', '');
        const description = (frontmatter.description || '').replace(/^["']|["']$/g, '');

        // Skip files without proper frontmatter
        if (!frontmatter.description && !frontmatter.name) continue;

        const stage = determineStage(agentId);

        // Extract content from body
        const purpose = extractPurpose(body, description);
        const capabilities = extractCapabilities(body);
        const workflow = extractWorkflow(body);

        // Build example from capabilities or stage
        const example = capabilities.length > 0
          ? `Capabilities: ${capabilities.slice(0, 3).join(', ')}`
          : `Spawned during ${stage} stage`;

        agents.push({
          id: agentId,
          name: frontmatter.name ? formatAgentName(frontmatter.name) : formatAgentName(agentId),
          type: 'agent',
          description: description,
          model: frontmatter.model || 'sonnet',
          checkpoint: null,
          path: `.claude/agents/${file}`,
          tools: parseTools(frontmatter['allowed-tools']),
          color: determineColor(stage),
          stage: stage,
          loads_skills: [],
          spawned_by: [],
          frontmatter: {
            model: frontmatter.model || 'sonnet',
            checkpoint: null,
            color: determineColor(stage),
            loads_skills: [],
            spawned_by: [],
            hooks: hooks,
          },
          rawContent: body,
          content: {
            purpose: purpose || description,
            example: example,
            workflow: workflow || 'See agent documentation for detailed workflow'
          }
        });
      } catch (err) {
        console.error(`Error parsing agent ${file}:`, err);
      }
    }

    // Sort by stage then name
    agents.sort((a, b) => {
      const stageOrder = ['Discovery', 'Prototype', 'ProductSpecs', 'SolArch', 'Implementation', 'Quality', 'GRC', 'Process', 'Reflexion', 'Traceability', 'Utility'];
      const stageCompare = stageOrder.indexOf(a.stage) - stageOrder.indexOf(b.stage);
      if (stageCompare !== 0) return stageCompare;
      return a.name.localeCompare(b.name);
    });

    return NextResponse.json(agents);
  } catch (error) {
    console.error('Error loading agents:', error);
    return NextResponse.json([]);
  }
}
