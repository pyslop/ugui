from . import Component
from .material_icon import MaterialIcon
from ugui.html import Element


class Box(Component):
    def __init__(self, **props):
        material_icon = props.pop("material_icon", None)
        icon_size = props.pop("icon_size", "2.5rem")
        icon_color = props.pop("icon_color", None)
        props["class"] = f"box"

        super().__init__("div", **props)

        # Create container for content
        self.content_box = Element("div", cls="box-content")

        # Handle material icon if specified
        if material_icon:
            icon = MaterialIcon(
                name=material_icon,
                size=icon_size,
                color=icon_color,
            )
            icon_wrapper = Element("div", cls="box-icon")
            icon_wrapper.append(icon)
            self.append(icon_wrapper)

        self.append(self.content_box)

    def __enter__(self):
        if self._page:
            self._page._current = self.content_box
            self.content_box._page = self._page
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            self._page._current = self.parent

    def style(self) -> str:
        return """
        .box {
            display: flex;
            align-items: flex-start;
            gap: 1.5rem;
            padding: 1.5rem;
            background: var(--color-bg);
            border-radius: 0.5rem;
            box-shadow: 0 0 1rem var(--color-shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .box:hover {
            transform: translateY(-2px);
            box-shadow: 0 0.5rem 2rem var(--color-shadow-hover);
        }
        .box-icon {
            flex: 0 0 auto;
            color: var(--color-primary);
            transition: transform 0.2s ease;
        }
        .box:hover .box-icon {
            transform: scale(1.1);
            color: var(--color-primary-hover);
        }
        .box-content {
            flex: 1;
            min-width: 0;
        }
        .box-content h3 {
            margin-bottom: 0.5rem;
            color: var(--color-primary);
        }
        """
