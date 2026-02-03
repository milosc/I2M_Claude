import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface SkillContent {
  purpose: string;
  example: string;
  workflow: string;
}

interface FrontmatterAttributes {
  model?: string | null;
  context?: string | null;
  agent?: string | null;
  allowed_tools?: string[];
  skills_required?: string[];
  [key: string]: unknown;
}

interface Skill {
  id: string;
  name: string;
  type: 'skill';
  description: string;
  stage: string;
  path: string;
  model: string | null;
  context: string | null;
  agent: string | null;
  allowed_tools: string[];
  skills_required: string[];
  frontmatter: FrontmatterAttributes;
  rawContent: string;
  content: SkillContent;
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
  // Look for ## Section Name or ### Section Name
  const patterns = [
    new RegExp(`##\\s*${sectionName}[\\s\\S]*?(?=\\n##|$)`, 'i'),
    new RegExp(`###\\s*${sectionName}[\\s\\S]*?(?=\\n###|\\n##|$)`, 'i'),
  ];

  for (const pattern of patterns) {
    const match = body.match(pattern);
    if (match) {
      // Remove the header line and return content
      return match[0].replace(/^##?\s*[^\n]+\n/, '').trim();
    }
  }
  return '';
}

function extractWhenToUse(body: string): string[] {
  const section = extractSection(body, 'When to Use(?: This Skill)?');
  if (!section) return [];

  // Extract bullet points
  const bullets = section.match(/^[-*]\s+(.+)$/gm);
  if (bullets) {
    return bullets.map(b => b.replace(/^[-*]\s+/, '').trim());
  }
  return [];
}

function extractPurpose(body: string, description: string): string {
  // Try to find first paragraph after the title
  const titleMatch = body.match(/^#\s+[^\n]+\n\n([^\n#]+)/);
  if (titleMatch) {
    return titleMatch[1].trim();
  }
  // Fall back to description
  return description;
}

function extractWorkflow(body: string): string {
  // Look for workflow, execution, or process sections
  const workflowSection = extractSection(body, 'Workflow|Execution|Process|The Method|How It Works');
  if (workflowSection) {
    // Limit to reasonable length
    return workflowSection.substring(0, 500);
  }
  return '';
}

function determineStage(skillName: string): string {
  const name = skillName.toLowerCase();
  if (name.startsWith('discovery_') || name.startsWith('discovery-')) return 'Discovery';
  if (name.startsWith('prototype_') || name.startsWith('prototype-')) return 'Prototype';
  if (name.startsWith('productspecs_') || name.startsWith('productspecs-')) return 'ProductSpecs';
  if (name.startsWith('solarch_') || name.startsWith('solarch-') || name.startsWith('solutionarchitecture_')) return 'SolArch';
  if (name.startsWith('implementation_') || name.startsWith('implementation-')) return 'Implementation';
  if (name.startsWith('grc_')) return 'GRC';
  if (name.startsWith('security_')) return 'Security';
  if (name.startsWith('shared_')) return 'Shared';
  return 'Utility';
}

function parseAllowedTools(value: string | undefined): string[] {
  if (!value) return [];
  return value.split(',').map(t => t.trim()).filter(Boolean);
}

function formatSkillName(name: string): string {
  return name
    .split(/[-_]/)
    .map((w: string) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

export async function GET() {
  try {
    // Navigate to project root (.claude folder is at project root)
    // 04-implementation -> Prototype_ClaudeManual -> claudeManual (2 levels up)
    const projectRoot = path.resolve(process.cwd(), '../..');
    const skillsDir = path.join(projectRoot, '.claude', 'skills');

    if (!fs.existsSync(skillsDir)) {
      console.error('Skills directory not found:', skillsDir);
      return NextResponse.json([]);
    }

    const skills: Skill[] = [];
    const entries = fs.readdirSync(skillsDir, { withFileTypes: true });

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;

      const skillMdPath = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillMdPath)) continue;

      try {
        const fileContent = fs.readFileSync(skillMdPath, 'utf-8');
        const { frontmatter, body } = parseYamlFrontmatter(fileContent);

        const skillId = entry.name;
        const skillName = frontmatter.name || skillId;
        const description = (frontmatter.description || '').replace(/^["']|["']$/g, '');

        // Extract content from body
        const purpose = extractPurpose(body, description);
        const whenToUse = extractWhenToUse(body);
        const workflow = extractWorkflow(body);

        // Build example from whenToUse or description
        const example = whenToUse.length > 0
          ? `Use when: ${whenToUse.slice(0, 3).join(', ')}`
          : `Invoke via: /${skillName}`;

        skills.push({
          id: skillId,
          name: formatSkillName(skillName),
          type: 'skill',
          description: description,
          stage: determineStage(skillId),
          path: `.claude/skills/${entry.name}/SKILL.md`,
          model: frontmatter.model || null,
          context: frontmatter.context || null,
          agent: frontmatter.agent || null,
          allowed_tools: parseAllowedTools(frontmatter['allowed-tools']),
          skills_required: [],
          frontmatter: {
            model: frontmatter.model || null,
            context: frontmatter.context || null,
            agent: frontmatter.agent || null,
            allowed_tools: parseAllowedTools(frontmatter['allowed-tools']),
            skills_required: [],
          },
          rawContent: body,
          content: {
            purpose: purpose || description,
            example: example,
            workflow: workflow || 'See SKILL.md for detailed workflow'
          }
        });
      } catch (err) {
        console.error(`Error parsing skill ${entry.name}:`, err);
      }
    }

    // Sort by stage then name
    skills.sort((a, b) => {
      const stageOrder = ['Discovery', 'Prototype', 'ProductSpecs', 'SolArch', 'Implementation', 'GRC', 'Security', 'Shared', 'Utility'];
      const stageCompare = stageOrder.indexOf(a.stage) - stageOrder.indexOf(b.stage);
      if (stageCompare !== 0) return stageCompare;
      return a.name.localeCompare(b.name);
    });

    return NextResponse.json(skills);
  } catch (error) {
    console.error('Error loading skills:', error);
    return NextResponse.json([]);
  }
}
