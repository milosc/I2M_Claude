import React, { useState, useEffect, Suspense, lazy } from 'react';
import {
  Dialog,
  DialogContainer,
  Heading,
  Button,
  Tabs,
  TabList,
  TabPanels,
  Item,
  View,
  Link,
  Content,
  ProgressCircle,
} from '@adobe/react-spectrum';
import Close from '@spectrum-icons/workflow/Close';
import Star from '@spectrum-icons/workflow/Star';
import StarOutline from '@spectrum-icons/workflow/StarOutline';
import Copy from '@spectrum-icons/workflow/Copy';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

// Lazy load Mermaid renderer for performance
const MermaidRenderer = lazy(() => import('../components/MermaidRenderer'));
const MarkdownRenderer = lazy(() => import('../components/MarkdownRenderer'));

/**
 * Component Detail Modal Screen (SCR-006)
 *
 * Full-screen modal for deep-dive into component documentation with tabbed interface.
 * Uses Adobe Spectrum React components for Assembly-First compliance.
 *
 * @component
 * @example
 * ```tsx
 * <ComponentDetailModal
 *   isOpen={true}
 *   componentId="Discovery_JTBD"
 *   componentType="Skill"
 *   onClose={() => setIsOpen(false)}
 * />
 * ```
 */

// ═══════════════════════════════════════════════════════════════
// TYPE DEFINITIONS
// ═══════════════════════════════════════════════════════════════

type ComponentType = 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc';

type TabKey = 'purpose' | 'examples' | 'options' | 'workflow' | 'traceability';

interface ComponentDetailModalProps {
  isOpen: boolean;
  componentId: string | null;
  componentType: ComponentType | null;
  onClose: () => void;
}

interface ComponentData {
  id: string;
  name: string;
  description: string;
  path: string;
  stage?: string;
  content?: {
    purpose?: string;
    usage?: string;
    example?: string;
    options?: string;
    workflow?: string;
  };
}

interface FetchComponentResponse {
  data: ComponentData;
  related: any[];
}

// ═══════════════════════════════════════════════════════════════
// VALIDATION SCHEMAS
// ═══════════════════════════════════════════════════════════════

const modalPropsSchema = z.object({
  componentId: z.string().min(1),
  componentType: z.enum(['Skill', 'Command', 'Agent', 'Rule', 'Hook', 'Workflow', 'WaysOfWorking', 'ArchitectureDoc']),
  isOpen: z.boolean(),
  onClose: z.function(),
});

// ═══════════════════════════════════════════════════════════════
// API FUNCTIONS
// ═══════════════════════════════════════════════════════════════

async function fetchComponent(
  type: ComponentType,
  id: string
): Promise<FetchComponentResponse> {
  const endpoint = `/api/${type.toLowerCase()}s/${id}`;
  const response = await fetch(endpoint);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Component not found');
    }
    throw new Error('Failed to fetch component');
  }

  return response.json();
}

async function toggleFavorite(componentId: string, isFavorited: boolean): Promise<void> {
  const method = isFavorited ? 'DELETE' : 'POST';
  const endpoint = isFavorited
    ? `/api/preferences/favorites/${componentId}`
    : '/api/preferences/favorites';

  const response = await fetch(endpoint, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: !isFavorited ? JSON.stringify({ id: componentId }) : undefined,
  });

  if (!response.ok) {
    throw new Error('Failed to update favorites');
  }
}

function checkIsFavorited(componentId: string): boolean {
  const favoritesData = localStorage.getItem('claudemanual:favorites');
  if (!favoritesData) return false;

  try {
    const { favorites } = JSON.parse(favoritesData);
    return favorites.some((fav: any) => fav.id === componentId);
  } catch {
    return false;
  }
}

function updateLastViewed(componentId: string, componentType: ComponentType): void {
  const lastViewed = {
    id: componentId,
    type: componentType,
    timestamp: Date.now(),
  };
  localStorage.setItem('claudemanual:last_viewed', JSON.stringify(lastViewed));
}

// ═══════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

function generateTraceabilityContent(
  componentType: ComponentType,
  componentData: ComponentData,
  relatedData: any[]
): string {
  let markdown = `# Traceability\n\n`;
  markdown += `**Component ID**: ${componentData.id}\n`;
  markdown += `**Type**: ${componentType}\n`;
  markdown += `**Path**: \`${componentData.path}\`\n`;
  markdown += `**Stage**: ${componentData.stage || 'N/A'}\n\n`;

  if (componentType === 'Skill') {
    markdown += `## Dependencies\n\n`;
    markdown += `No skill dependencies.\n`;
    markdown += `\n## Used By\n\n`;
    if (relatedData.length > 0) {
      relatedData.forEach((item) => {
        markdown += `- ${item.type}: [${item.name}](#)\n`;
      });
    } else {
      markdown += `Not used by any commands or agents.\n`;
    }
  }

  if (componentType === 'Command') {
    markdown += `## Invokes Skills\n\n`;
    markdown += `See related skills in documentation.\n`;
    markdown += `\n## Spawns Agents\n\n`;
    markdown += `See related agents in documentation.\n`;
  }

  return markdown;
}

async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════

export function ComponentDetailModalScreen({
  isOpen,
  componentId,
  componentType,
  onClose,
}: ComponentDetailModalProps) {
  const queryClient = useQueryClient();
  const [selectedTab, setSelectedTab] = useState<TabKey>('purpose');
  const [isFavorited, setIsFavorited] = useState<boolean>(false);
  const [copySuccess, setCopySuccess] = useState<boolean>(false);

  // Fetch component data
  const { data, isLoading, error } = useQuery({
    queryKey: ['component', componentType, componentId],
    queryFn: () => fetchComponent(componentType!, componentId!),
    enabled: isOpen && !!componentId && !!componentType,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Favorite mutation
  const favoriteMutation = useMutation({
    mutationFn: () => toggleFavorite(componentId!, isFavorited),
    onSuccess: () => {
      setIsFavorited(!isFavorited);
      queryClient.invalidateQueries({ queryKey: ['preferences'] });
    },
  });

  // Initialize favorited state
  useEffect(() => {
    if (componentId) {
      setIsFavorited(checkIsFavorited(componentId));
    }
  }, [componentId]);

  // Update last viewed
  useEffect(() => {
    if (isOpen && componentId && componentType) {
      updateLastViewed(componentId, componentType);
    }
  }, [isOpen, componentId, componentType]);

  // Reset tab on modal open
  useEffect(() => {
    if (isOpen) {
      setSelectedTab('purpose');
    }
  }, [isOpen]);

  // Copy path handler
  const handleCopyPath = async () => {
    if (data?.data?.path) {
      const success = await copyToClipboard(data.data.path);
      if (success) {
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      }
    }
  };

  // Generate tab content
  const tabContent = React.useMemo(() => {
    if (!data?.data) return null;

    const componentData = data.data;

    return {
      purpose: componentData.content?.purpose || 'No purpose defined.',
      examples: componentData.content?.example || 'No examples available.',
      options: componentData.content?.options || 'No options defined.',
      workflow: componentData.content?.workflow || 'No workflow diagram available.',
      traceability: generateTraceabilityContent(
        componentType!,
        componentData,
        data.related || []
      ),
    };
  }, [data, componentType]);

  // ═══════════════════════════════════════════════════════════════
  // RENDER
  // ═══════════════════════════════════════════════════════════════

  return (
    <DialogContainer onDismiss={onClose}>
      {isOpen && (
        <Dialog size="L" isDismissable>
          <Heading id="modal-title" level={2}>
            {data?.data?.name || 'Loading...'}
          </Heading>

          {/* Header Actions */}
          <Content marginTop="size-100">
            <View
              UNSAFE_style={{
                display: 'flex',
                gap: '8px',
                alignItems: 'center',
              }}
            >
              <Link
                onPress={handleCopyPath}
                UNSAFE_style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <Copy size="S" />
                {copySuccess ? 'Copied!' : 'Copy Path'}
              </Link>

              <Button
                variant="primary"
                onPress={() => favoriteMutation.mutate()}
                isDisabled={favoriteMutation.isPending}
              >
                {isFavorited ? <Star size="S" /> : <StarOutline size="S" />}
              </Button>

              <Button
                variant="secondary"
                onPress={onClose}
                UNSAFE_style={{ marginLeft: 'auto' }}
              >
                <Close size="S" />
              </Button>
            </View>
          </Content>

          {/* Loading State */}
          {isLoading && (
            <Content>
              <View padding="size-400">
                <ProgressCircle aria-label="Loading component data" isIndeterminate />
              </View>
            </Content>
          )}

          {/* Error State */}
          {error && (
            <Content>
              <View padding="size-400">
                <p style={{ color: 'var(--spectrum-global-color-red-500)' }}>
                  {error.message || 'Failed to load component'}
                </p>
              </View>
            </Content>
          )}

          {/* Tabs */}
          {data?.data && tabContent && (
            <Content>
              <Tabs
                aria-label="Component details"
                selectedKey={selectedTab}
                onSelectionChange={(key) => setSelectedTab(key as TabKey)}
              >
                <TabList>
                  <Item key="purpose">Purpose</Item>
                  <Item key="examples">Examples</Item>
                  <Item key="options">Options</Item>
                  <Item key="workflow">Workflow</Item>
                  <Item key="traceability">Traceability</Item>
                </TabList>

                <TabPanels>
                  <Item key="purpose">
                    <View padding="size-400">
                      <Suspense fallback={<ProgressCircle isIndeterminate />}>
                        <MarkdownRenderer content={tabContent.purpose} />
                      </Suspense>
                    </View>
                  </Item>

                  <Item key="examples">
                    <View padding="size-400">
                      <Suspense fallback={<ProgressCircle isIndeterminate />}>
                        <MarkdownRenderer content={tabContent.examples} />
                      </Suspense>
                    </View>
                  </Item>

                  <Item key="options">
                    <View padding="size-400">
                      <Suspense fallback={<ProgressCircle isIndeterminate />}>
                        <MarkdownRenderer content={tabContent.options} />
                      </Suspense>
                    </View>
                  </Item>

                  <Item key="workflow">
                    <View padding="size-400">
                      <Suspense fallback={<ProgressCircle isIndeterminate />}>
                        {tabContent.workflow.includes('```mermaid') ? (
                          <MermaidRenderer content={tabContent.workflow} />
                        ) : (
                          <MarkdownRenderer content={tabContent.workflow} />
                        )}
                      </Suspense>
                    </View>
                  </Item>

                  <Item key="traceability">
                    <View padding="size-400">
                      <Suspense fallback={<ProgressCircle isIndeterminate />}>
                        <MarkdownRenderer content={tabContent.traceability} />
                      </Suspense>
                    </View>
                  </Item>
                </TabPanels>
              </Tabs>
            </Content>
          )}
        </Dialog>
      )}
    </DialogContainer>
  );
}

export default ComponentDetailModalScreen;
