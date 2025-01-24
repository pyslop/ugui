from . import Component
from pathlib import Path
from ugui.html import TextNode


def load_svg(name: str) -> str:
    """Load an SVG file from the static/material-icons directory"""
    base_dir = Path(__file__).parent.parent
    icon_path = base_dir / "static" / "material-icons" / f"{name}.svg"
    if not icon_path.exists():
        raise ValueError(f"Icon {name} not found at {icon_path}")
    return icon_path.read_text()


class MaterialIcon(Component):
    def __init__(self, **props):
        name = props.pop("name", "")
        size = props.pop("size", "1.5rem")
        color = props.pop("color", "currentColor")

        # Combine classes properly
        base_class = f"material-icon icon-{name}"
        if "cls" in props:
            base_class = f"{base_class} {props.pop('cls')}"
        if "class" in props:
            base_class = f"{base_class} {props.pop('class')}"

        # Load SVG content
        svg_content = load_svg(name)

        # Initialize with combined classes
        super().__init__("span", cls=base_class, **props)

        # Add SVG with styling
        self.append(
            TextNode(
                svg_content.replace(
                    "<svg",
                    f'<svg style="width: {size}; height: {size}; fill: {color}"',
                    1,
                ),
                raw=True,
            )
        )

    def style(self) -> str:
        return """
        .material-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            vertical-align: middle;
        }
        .material-icon svg {
            display: block;
        }
        """
