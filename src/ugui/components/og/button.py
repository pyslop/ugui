from . import Component
from .material_icon import MaterialIcon


class Button(Component):
    def __init__(self, text=None, **props):
        # Extract and combine class names first
        material_icon = props.pop("material_icon", None)
        contents = props.pop("contents", [])
        props["class"] = "btn"

        # Initialize with combined class and remaining props
        super().__init__("button", **props)

        # Handle material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size="1.8rem")
            self.append(icon)

        if text:
            self.append(text)
        elif isinstance(contents, (list, tuple)):
            for content in contents:
                if isinstance(content, MaterialIcon):
                    # Skip material icons in contents as they should be handled via material_icon prop
                    continue
                if content is not None:
                    self.append(content)
        elif contents is not None:
            self.append(contents)

    def style(self) -> str:
        return """
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--color-primary);
            color: var(--color-bg);
            text-decoration: none;
            border-radius: 0.25rem;
            margin: 0.5rem;
            border: none;
            cursor: pointer;  /* Always show pointer for buttons */
            transition: all 0.2s ease;
            position: relative;
            box-shadow: 0 2px 4px var(--color-shadow);
            transform: translateY(0);
        }
        .btn:hover {
            background: var(--color-primary-hover);
            box-shadow: 0 4px 8px var(--color-shadow-hover);
            transform: translateY(-1px);
        }
        .btn:active {
            transform: translateY(1px);
            box-shadow: 0 1px 2px var(--color-shadow);
        }
        .btn.secondary {
            background: transparent;
            border: 1px solid var(--color-primary);
            color: var(--color-primary);
            box-shadow: none;
        }
        .btn.secondary:hover {
            background: var(--color-primary-bg);
            border-color: var(--color-primary-hover);
            color: var(--color-primary-hover);
            box-shadow: 0 2px 4px var(--color-shadow);
        }
        .btn.secondary:active {
            background: var(--color-primary-bg-hover);
            transform: translateY(1px);
            box-shadow: none;
        }
        .btn .material-icon {
            margin-right: -0.25rem;
            margin-left: -0.25rem;
            transition: transform 0.2s ease;
        }
        .btn:hover .material-icon {
            transform: scale(1.1);
        }
        .btn:active .material-icon {
            transform: scale(0.95);
        }
        """
