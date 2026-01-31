# Assembly-First Component Library

This library is a self-contained "Prototyping Engine" designed for high-efficiency UI generation by LLMs. It uses **React Aria Components** as its accessible foundation and **Tailwind CSS** for styling.

## Structure

- `src/`: The core accessible component logic.
- `stories/`: Visual documentation and interaction examples (Storybook).
- `specs/`: 
    - `accessibility/`: WAI-ARIA design patterns and keyboard interaction specs.
    - `api/`: Prop definitions and component interfaces.
    - `test/`: Technical unit tests.
- `themes/`: Tailwind CSS plugin and theme configuration.
- `templates/`: Starter configurations (e.g., `tailwind.config.js`).
- `examples/`: Reference implementations for complex screens.
- `LLM_INSTRUCTIONS/`: The "Brain" for the LLM. Contains `SKILL.md` and `INTERACTIONS.md`.

## For the LLM (Senior UI Engineer)

When using this library to generate screens:
1.  **Always** read `LLM_INSTRUCTIONS/SKILL.md` first.
2.  Consult `specs/api/` for correct prop usage.
3.  Consult `specs/accessibility/` to ensure compliant keyboard and screen reader behavior.
4.  Use the `INTERACTIONS.md` guide for styling states (`isHovered`, `isFocusVisible`, etc.).

## Maintenance

To update this library:
1.  Add/Modify components in `src/`.
2.  Add corresponding stories in `stories/`.
3.  Update the `manifests/components.json` registry.
4.  Ensure `specs/api/` and `specs/accessibility/` are updated to reflect changes.
