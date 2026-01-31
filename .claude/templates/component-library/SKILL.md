# Component Library Skill

## Mission
You are a Senior UI Engineer orchestrating a design system. Your goal is to build high-quality, accessible, and consistent UIs using the pre-built components in this library. Do not re-invent the wheel.

## Strict Usage Protocol

1.  **Discovery:** Before writing any UI code, you MUST:
    *   Check `manifests/components.json` for available components.
    *   Read the **API Specs** in `specs/api/` to understand prop types and valid values.
    *   Read the **Accessibility Specs** in `specs/accessibility/` to ensure the generated UI follows the correct ARIA patterns.
    *   Review the relevant **Storybook stories** in `stories/` to see visual variants and interaction examples.
2.  **Constraint:** You are FORBIDDEN from writing raw HTML elements (like `div`, `input`, `button`) if a library component exists (e.g., `Button`, `TextField`, `ComboBox`).
3.  **Implementation:**
    *   Import components from the library source: `import { Button } from '../src';` (adjust path as needed).
    *   **Advanced Capabilities:** You now have access to **Spectrum V3 components** (prefixed or direct from `@adobe/react-spectrum`), **React Stately hooks** for complex state management, and **Internationalization utilities** (date, number, and string formatting).
    *   Focus on "Glue Code": fetching data, managing state (using `react-stately` hooks if needed), and passing data to components.
    *   Use `className` with Tailwind CSS utilities for layout and spacing overrides ONLY. Do not write custom CSS classes unless absolutely necessary.
4.  **Accessibility:** The components handle ARIA attributes and keyboard interactions. Do not manually add `role`, `aria-label`, etc., unless the component documentation explicitly asks for it (e.g., for icon-only buttons).

## Styling Strategy (Tailwind)

*   This library uses `react-aria-components` with Tailwind CSS.
*   Components accept `className` which can be a string or a function receiving the render state (e.g., `({isHovered, isSelected}) => ...`).
*   Use the provided themes and tokens found in `themes/`.

## Workflow for Generating Screens

1.  **Analyze Requirements:** Identify the needed UI elements.
2.  **Map to Components:** Select the matching components from the library.
3.  **Data Modeling:** Define the data structure needed for the components (e.g., `items` array for a `ComboBox`).
4.  **Assembly:** Compose the components using the composition pattern.
    *   **CRITICAL:** React Aria Components use composition with child components for labels and inputs. DO NOT use `label` as a prop.
    *   Example:
        ```tsx
        import { Form, TextField, Label, Input, Button } from '../src';

        export function LoginForm({ onSubmit }) {
          return (
            <Form onSubmit={onSubmit} className="flex flex-col gap-4">
              <TextField name="email" type="email" isRequired className="flex flex-col gap-1">
                <Label>Email</Label>
                <Input />
              </TextField>
              <TextField name="password" type="password" isRequired className="flex flex-col gap-1">
                <Label>Password</Label>
                <Input />
              </TextField>
              <Button type="submit">Sign In</Button>
            </Form>
          );
        }
        ```
    *   **NumberField Example:**
        ```tsx
        import { NumberField, Label, Group, Button, Input } from '../src';

        <NumberField minValue={0} maxValue={200} defaultValue={120}>
          <Label>Blood Pressure</Label>
          <Group className="flex gap-2">
            <Button slot="decrement">-</Button>
            <Input />
            <Button slot="increment">+</Button>
          </Group>
        </NumberField>
        ```
    *   **DateField Example:**
        ```tsx
        import { DateField, Label, DateInput, DateSegment } from '../src';
        import { parseDate } from '@internationalized/date';

        <DateField defaultValue={parseDate('2024-01-01')} isRequired>
          <Label>Date of Birth</Label>
          <DateInput className="flex gap-1">
            {segment => <DateSegment segment={segment} />}
          </DateInput>
        </DateField>
        ```
        **CRITICAL:** DateField uses `DateValue` types from `@internationalized/date`, NOT JavaScript `Date` objects. Use `parseDate()`, `parseDateTime()`, or `parseZonedDateTime()` for default values.
    *   **Select Example:**
        ```tsx
        import { Select, Label, Button, SelectValue, ListBox, ListBoxItem } from '../src';

        <Select>
          <Label>Insurance Type</Label>
          <Button>
            <SelectValue />
          </Button>
          <Popover>
            <ListBox>
              <ListBoxItem>Private</ListBoxItem>
              <ListBoxItem>Medicare</ListBoxItem>
              <ListBoxItem>Self-Pay</ListBoxItem>
            </ListBox>
          </Popover>
        </Select>
        ```
