from . import Component
from .material_icon import MaterialIcon
from ugui.html import Element


class Link(Component):
    def __init__(self, **props):
        # Extract link-specific props
        text = props.pop("text", "")
        url = props.pop("url", "#")
        material_icon = props.pop("material_icon", None)
        icon_position = props.pop("icon_position", "left")
        icon_size = props.pop("icon_size", "1.8rem")
        # cls = f"link {props.pop('class', '')} {props.pop('cls', '')}".strip()
        props["class"] = "link"

        # Initialize with link attributes
        super().__init__("a", href=url, **props)

        # Add text content first in a span
        text_span = Element("span", cls="link-text")
        text_span.append(text)
        self.append(text_span)

        # Add icon with proper ordering class
        if material_icon:
            icon_span = MaterialIcon(
                name=material_icon,
                size=icon_size,
                cls=f"link-icon link-icon-{icon_position}",
            )
            self.append(icon_span)

    def style(self) -> str:
        return """
        .link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #0066cc;
            text-decoration: none;
            white-space: nowrap;
        }
        .link:hover {
            text-decoration: underline;
        }
        .link .link-icon {
            display: inline-flex;
            color: inherit;
            opacity: 0.8;
        }
        .link:hover .link-icon {
            opacity: 1;
        }
        .link .link-icon-left {
            order: -1;  /* Place before text */
        }
        .link .link-icon-right {
            order: 1;   /* Place after text */
        }
        .link .link-text {
            order: 0;   /* Keep text in middle */
            display: inline-block;
            line-height: 1;
        }
        """
