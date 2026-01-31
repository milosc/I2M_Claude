const modules = import.meta.glob('./*.json', { eager: true });
const messages: Record<string, any> = {};

for (const path in modules) {
  // Extract locale from path ./en-US.json -> en-US
  const locale = path.replace('./', '').replace('.json', '');
  messages[locale] = (modules[path] as any).default || modules[path];
}

export default messages;
