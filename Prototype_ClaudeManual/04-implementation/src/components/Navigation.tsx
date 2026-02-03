'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Explorer', icon: '📁' },
    { href: '/search', label: 'Search', icon: '🔍' },
    { href: '/favorites', label: 'Favorites', icon: '⭐' },
    { href: '/workflow', label: 'Workflows', icon: '🔄' },
    { href: '/architecture', label: 'Architecture', icon: '🏗️' },
    { href: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <nav className="border-b border-border bg-surface-1" aria-label="Main navigation">
      <div className="flex items-center gap-1 px-4 py-2 overflow-x-auto">
        {links.map((link) => {
          const isActive = pathname === link.href || (link.href !== '/' && pathname?.startsWith(link.href));
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-2 px-3 py-2 rounded whitespace-nowrap transition-colors ${
                isActive
                  ? 'bg-accent-default text-white'
                  : 'hover:bg-surface-2 text-secondary hover:text-primary'
              }`}
              aria-current={isActive ? 'page' : undefined}
            >
              <span aria-hidden="true">{link.icon}</span>
              <span className="text-sm font-medium">{link.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
