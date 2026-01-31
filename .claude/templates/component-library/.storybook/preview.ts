import type { Preview } from "@storybook/react";
import '../stories/styles.css'; // Import global styles
import '../stories/themes.css'; // Import new theme variables

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme for components',
      defaultValue: 'graphite-light',
      toolbar: {
        icon: 'circlehollow',
        items: [
          { value: 'graphite-light', title: 'Graphite Light' },
          { value: 'graphite-dark', title: 'Graphite Dark' },
          { value: 'ocean-light', title: 'Ocean Light' },
          { value: 'ocean-dark', title: 'Ocean Dark' },
          { value: 'forest-light', title: 'Forest Light' },
          { value: 'forest-dark', title: 'Forest Dark' },
        ],
        showName: true,
      },
    },
    highContrast: {
      name: 'High Contrast',
      description: 'Force high contrast borders and text',
      defaultValue: 'false',
      toolbar: {
        icon: 'eye',
        items: [
          { value: 'false', title: 'Normal' },
          { value: 'true', title: 'High Contrast' },
        ],
        showName: true,
      },
    },
  },
  decorators: [
    (Story, context) => {
      const theme = context.globals.theme || 'graphite-light';
      const highContrast = context.globals.highContrast || 'false';
      document.body.setAttribute('data-theme', theme);
      document.body.setAttribute('data-hc', highContrast);
      return Story();
    },
  ],
};

export default preview;
