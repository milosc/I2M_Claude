# Component Interaction Guidelines for LLM

## State Management
React Aria Components use a "Render Props" or "State Function" pattern for styling and content. You should utilize these to handle interactions without unnecessary `useState`.

### Styling States
Most components accept a function for `className` or `children` that provides the current state:
```tsx
<Button
  className={({ isPressed, isHovered, isFocusVisible }) =>
    `px-4 py-2 rounded ${isPressed ? 'bg-blue-700' : 'bg-blue-500'} ${isFocusVisible ? 'ring-2' : ''}`
  }
>
  Press Me
</Button>
```

### Common States to Handle
- **isHovered**: When the pointer is over the element.
- **isPressed**: When the element is being activated (mouse down/touch start).
- **isFocused**: When the element has keyboard or pointer focus.
- **isFocusVisible**: Specifically for keyboard focus (important for accessibility).
- **isDisabled**: When the component should not be interactive.
- **isSelected**: For toggleable components (Tabs, ListBox, Checkbox).

## Handling API Calls
When connecting components to real APIs:
1.  **Loading States**: Use the `isPending` prop (where available) or wrap components in a way that shows a `ProgressBar` or `ProgressCircle`.
2.  **Validation**: Use the `validationState` prop and `FieldError` component to display server-side or client-side errors.
3.  **Async Collections**: For components like `ComboBox` or `Select` that fetch data, use the `items` prop and manage the loading state via a custom hook (e.g., using `useAsyncList` from `react-stately`).

### Example: Async Search
```tsx
import { ComboBox, Item, Label, Input, Popover, ListBox } from '../src';
import { useAsyncList } from 'react-stately';

export function UserSearch() {
  let list = useAsyncList({
    async load({ filterText }) {
      let res = await fetch(`https://api.example.com/users?q=${filterText}`);
      let json = await res.json();
      return { items: json.users };
    }
  });

  return (
    <ComboBox items={list.items} inputValue={list.filterText} onInputChange={list.setFilterText}>
      <Label>Search Users</Label>
      <Input />
      <Popover>
        <ListBox>
          {(item) => <Item key={item.id}>{item.name}</Item>}
        </ListBox>
      </Popover>
    </ComboBox>
  );
}
```
