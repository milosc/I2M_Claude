import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface CommandContent {
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
  PreToolUse?: HookMatcher[];
  PostToolUse?: HookMatcher[];
  Stop?: HookMatcher[];
  [key: string]: HookMatcher[] | undefined;
}

interface FrontmatterAttributes {
  model?: string | null;
  argument_hint?: string | null;
  allowed_tools?: string[];
  invokes_skills?: string[];
  skills_required?: string[];
  skills_optional?: string[];
  orchestrates_agents?: string[];
  hooks?: ParsedHooks;
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

interface ParsedSkills {
  required: string[];
  optional: string[];
}

function parseSkillsSection(frontmatterText: string): ParsedSkills {
  const skills: ParsedSkills = { required: [], optional: [] };

  // Find skills section
  const skillsMatch = frontmatterText.match(/^skills:\s*$/m);
  if (!skillsMatch) return skills;

  const startIdx = skillsMatch.index! + skillsMatch[0].length;
  const lines = frontmatterText.substring(startIdx).split('\n');

  let currentList: 'required' | 'optional' | null = null;

  for (const line of lines) {
    // Stop if we hit another top-level key (no leading whitespace)
    if (line && !line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      break;
    }

    const trimmed = line.trim();

    if (trimmed === 'required:') {
      currentList = 'required';
    } else if (trimmed === 'optional:') {
      currentList = 'optional';
    } else if (trimmed.startsWith('- ') && currentList) {
      const skillName = trimmed.substring(2).trim();
      skills[currentList].push(skillName);
    }
  }

  return skills;
}

function parseHooksSection(frontmatterText: string): ParsedHooks | undefined {
  // Find hooks section
  const hooksMatch = frontmatterText.match(/^hooks:\s*$/m);
  if (!hooksMatch) return undefined;

  const startIdx = hooksMatch.index! + hooksMatch[0].length;
  const lines = frontmatterText.substring(startIdx).split('\n');

  const hooks: ParsedHooks = {};
  let currentHookType: string | null = null;
  let currentMatcher: HookMatcher | null = null;
  let currentHookEntry: Partial<HookEntry> | null = null;
  let inHooksArray = false;
  let commandLines: string[] = [];

  for (const line of lines) {
    // Stop if we hit another top-level key (no leading whitespace, has colon, not inside hooks)
    if (line && !line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      break;
    }

    const trimmed = line.trim();
    const indent = line.search(/\S/);

    // Hook type (PreToolUse:, Stop:, etc.) - 2 space indent
    if (indent === 2 && trimmed.endsWith(':') && !trimmed.startsWith('-')) {
      // Save previous hook entry
      if (currentHookEntry && currentHookEntry.type && currentMatcher) {
        if (commandLines.length > 0) {
          currentHookEntry.command = commandLines.join(' ').trim();
          commandLines = [];
        }
        currentMatcher.hooks.push(currentHookEntry as HookEntry);
        currentHookEntry = null;
      }
      // Save previous matcher
      if (currentMatcher && currentHookType) {
        if (!hooks[currentHookType]) hooks[currentHookType] = [];
        hooks[currentHookType]!.push(currentMatcher);
        currentMatcher = null;
      }

      currentHookType = trimmed.slice(0, -1);
      inHooksArray = false;
      continue;
    }

    // Array item start (- matcher: or - hooks:)
    if (trimmed.startsWith('- ') && currentHookType) {
      // Save previous hook entry
      if (currentHookEntry && currentHookEntry.type && currentMatcher) {
        if (commandLines.length > 0) {
          currentHookEntry.command = commandLines.join(' ').trim();
          commandLines = [];
        }
        currentMatcher.hooks.push(currentHookEntry as HookEntry);
        currentHookEntry = null;
      }
      // Save previous matcher if starting new one
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
      } else if (content.startsWith('hooks:')) {
        inHooksArray = true;
      } else if (content.startsWith('type:')) {
        currentHookEntry = { type: content.substring(5).trim() };
      }
      continue;
    }

    // Properties within matcher (once:, hooks:)
    if (currentMatcher && indent >= 6) {
      if (trimmed.startsWith('once:')) {
        currentMatcher.once = trimmed.substring(5).trim() === 'true';
      } else if (trimmed === 'hooks:') {
        inHooksArray = true;
      } else if (trimmed.startsWith('- type:')) {
        // Save previous hook entry
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
            // Multiline command starts
            commandLines = [];
          } else {
            currentHookEntry.command = cmdValue.replace(/^["']|["']$/g, '');
          }
        }
      } else if (commandLines !== null && currentHookEntry && !trimmed.startsWith('-') && !trimmed.includes(':')) {
        // Continuation of multiline command
        commandLines.push(trimmed);
      }
    }
  }

  // Save final entries
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

function parseYamlFrontmatter(content: string): { frontmatter: Record<string, string>; body: string; skills: ParsedSkills; hooks: ParsedHooks | undefined } {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!frontmatterMatch) return { frontmatter: {}, body: content, skills: { required: [], optional: [] }, hooks: undefined };

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

  // Parse skills section separately
  const skills = parseSkillsSection(frontmatterText);

  // Parse hooks section separately
  const hooks = parseHooksSection(frontmatterText);

  return { frontmatter, body: frontmatterMatch[2] || '', skills, hooks };
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
        const { frontmatter, body, skills, hooks } = parseYamlFrontmatter(fileContent);

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

        // Combine skills for invokes_skills (backward compatibility)
        const allSkills = [...skills.required, ...skills.optional];

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
          invokes_skills: allSkills,
          orchestrates_agents: [],
          frontmatter: {
            model: frontmatter.model || null,
            argument_hint: frontmatter['argument-hint'] || null,
            allowed_tools: parseAllowedTools(frontmatter['allowed-tools']),
            invokes_skills: allSkills,
            skills_required: skills.required.length > 0 ? skills.required : undefined,
            skills_optional: skills.optional.length > 0 ? skills.optional : undefined,
            orchestrates_agents: [],
            hooks: hooks,
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
