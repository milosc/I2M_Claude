'use client';

import React, { useState, useCallback, useEffect, useRef } from 'react';

export interface ResizableSidebarProps {
  /** Unique key for persisting width to localStorage */
  storageKey?: string;
  /** Minimum width in pixels */
  minWidth?: number;
  /** Maximum width in pixels */
  maxWidth?: number;
  /** Default width in pixels */
  defaultWidth?: number;
  /** Additional className for the sidebar */
  className?: string;
  /** Children to render inside the sidebar */
  children: React.ReactNode;
}

export const ResizableSidebar: React.FC<ResizableSidebarProps> = ({
  storageKey = 'sidebar-width',
  minWidth = 200,
  maxWidth = 600,
  defaultWidth = 320,
  className = '',
  children,
}) => {
  const [width, setWidth] = useState(defaultWidth);
  const [isResizing, setIsResizing] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);

  // Load saved width from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      const parsedWidth = parseInt(saved, 10);
      if (!isNaN(parsedWidth) && parsedWidth >= minWidth && parsedWidth <= maxWidth) {
        setWidth(parsedWidth);
      }
    }
  }, [storageKey, minWidth, maxWidth]);

  // Save width to localStorage when it changes
  useEffect(() => {
    if (!isResizing) {
      localStorage.setItem(storageKey, width.toString());
    }
  }, [width, isResizing, storageKey]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!isResizing || !sidebarRef.current) return;

      const sidebarRect = sidebarRef.current.getBoundingClientRect();
      const newWidth = e.clientX - sidebarRect.left;

      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setWidth(newWidth);
      }
    },
    [isResizing, minWidth, maxWidth]
  );

  const handleMouseUp = useCallback(() => {
    setIsResizing(false);
  }, []);

  // Add/remove event listeners for mouse move/up
  useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      // Prevent text selection while resizing
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'col-resize';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.userSelect = '';
      document.body.style.cursor = '';
    };
  }, [isResizing, handleMouseMove, handleMouseUp]);

  return (
    <aside
      ref={sidebarRef}
      className={`relative flex-shrink-0 border-r border-border overflow-y-auto ${className}`}
      style={{ width: `${width}px` }}
    >
      {/* Sidebar content */}
      <div className="h-full overflow-y-auto">{children}</div>

      {/* Resize handle */}
      <div
        onMouseDown={handleMouseDown}
        className={`absolute top-0 right-0 w-1 h-full cursor-col-resize group hover:bg-accent-default/30 transition-colors ${
          isResizing ? 'bg-accent-default/50' : ''
        }`}
        title="Drag to resize"
      >
        {/* Visual indicator on hover */}
        <div
          className={`absolute top-1/2 right-0 transform -translate-y-1/2 w-1 h-16 rounded-full opacity-0 group-hover:opacity-100 transition-opacity ${
            isResizing ? 'opacity-100 bg-accent-default' : 'bg-gray-400'
          }`}
        />
      </div>
    </aside>
  );
};

export default ResizableSidebar;
