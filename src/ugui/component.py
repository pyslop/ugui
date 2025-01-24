from pathlib import Path
from abc import abstractmethod
from typing import Any
from .html import Element, TextNode


def load_svg(name: str) -> str:
    """Load an SVG file from the static/material-icons directory"""
    base_dir = Path(__file__).parent
    icon_path = base_dir / "static" / "material-icons" / f"{name}.svg"
    if not icon_path.exists():
        raise ValueError(f"Icon {name} not found at {icon_path}")
    return icon_path.read_text()


class Component(Element):
    def __init__(self, _name: str = "div", **props):
        # Move title to data-tooltip and aria-label if present
        if "title" in props:
            tooltip = props.pop("title")
            if tooltip is not None:
                props["data-tooltip"] = tooltip
                props["aria-label"] = tooltip

        # Filter out None values from props
        filtered_props = {
            k: v for k, v in props.items() if k not in ["contents"] and v is not None
        }

        super().__init__(_name, **filtered_props)
        self.props = props

        # Initialize component styles
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                if content is not None:
                    self.append(content)
        elif contents is not None:
            self.append(contents)

    @abstractmethod
    def style(self) -> str:
        """Return the CSS for this component"""
        pass

    def __call__(self, page: Any) -> Any:
        """Make components callable for page context"""
        self._page = page
        if hasattr(page, "_current"):
            self.parent = page._current
            page._current.append(self)
        return self


class Card(Component):
    def __init__(self, **props):
        super().__init__("div", cls=f"card {props.get('class', '')}".strip(), **props)

        # Initialize section elements
        self._header = Element("div", cls="card-header")
        self._body = Element("div", cls="card-body")
        self._footer = Element("div", cls="card-footer")

        # Add default contents if provided
        if self.props.get("title"):
            self._header.append(self.props["title"])
            self.append(self._header)

        # Handle body contents
        contents = self.props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                self._body.append(content)
        else:
            self._body.append(contents)
        self.append(self._body)

        if self.props.get("footer"):
            self._footer.append(self.props["footer"])
            self.append(self._footer)

    def header(self, material_icon=None, **props):
        """Access the card header section"""
        if self._header not in self.children:
            self.children.insert(0, self._header)
        self._header._page = self._page

        # Add material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size="1.2rem", **props)
            self._header.children.insert(0, icon)

        return self._header

    def body(self):
        """Access the card body section"""
        self._body._page = self._page
        return self._body

    def footer(self, material_icon=None, **props):
        """Access the card footer section"""
        if self._footer not in self.children:
            self.append(self._footer)
        self._footer._page = self._page

        # Add material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size="1.2rem", **props)
            self._footer.children.insert(0, icon)

        return self._footer

    def style(self) -> str:
        return """
        .card {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            border: 0.0625rem solid #ddd;
            border-radius: 0.25rem;
            margin: 1rem 0;
            overflow: hidden;
        }
        .card-header {
            padding: 1rem;
            border-bottom: 0.0625rem solid #ddd;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card-body { padding: 1rem; }
        .card-footer {
            padding: 1rem;
            border-top: 0.0625rem solid #ddd;
            background: #f8f9fa;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        """


class Form(Component):
    def __init__(self, **props):
        # Extract form-specific props
        action = props.pop("action", "#")
        method = props.pop("method", "post")

        # Initialize with form attributes
        super().__init__("form", action=action, method=method, **props)

        # Handle contents after initialization
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                self.append(content)
        else:
            self.append(contents)

    def style(self) -> str:
        return """
        .form-field {
            margin-bottom: 1rem;
            width: 100%;
            box-sizing: border-box;
        }
        .form-field label {
            display: block;
            margin-bottom: 0.5rem;
        }
        .form-field input {
            box-sizing: border-box;
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        form { width: 100%; }
        """


class Button(Component):
    def __init__(self, **props):
        # Extract and combine class names first
        cls = f"btn {props.pop('class', '')} {props.pop('cls', '')}".strip()
        text = props.pop("text", "")
        material_icon = props.pop("material_icon", None)
        contents = props.pop("contents", [])

        # Initialize with combined class and remaining props
        super().__init__("button", cls=cls, **props)

        # Handle material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size="1.2rem")
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
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 0.25rem;
            margin: 0.5rem;
            border: none;
            cursor: pointer;  /* Always show pointer for buttons */
            transition: all 0.2s ease;
            position: relative;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transform: translateY(0);
        }
        .btn:hover {
            background: #0052a3;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transform: translateY(-1px);
        }
        .btn:active {
            transform: translateY(1px);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        .btn.secondary {
            background: transparent;
            border: 1px solid #0066cc;
            color: #0066cc;
            box-shadow: none;
        }
        .btn.secondary:hover {
            background: rgba(0, 102, 204, 0.1);
            border-color: #0052a3;
            color: #0052a3;
            box-shadow: 0 2px 4px rgba(0, 102, 204, 0.1);
        }
        .btn.secondary:active {
            background: rgba(0, 102, 204, 0.2);
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


class Fieldset(Component):
    def __init__(self, **props):
        # Extract fieldset-specific props
        legend = props.pop("legend", None)

        # Initialize with remaining props
        super().__init__("fieldset", **props)

        # Add legend if provided
        if legend:
            legend_elem = Element("legend")
            legend_elem.append(legend)
            self.append(legend_elem)

        # Handle contents after initialization
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                self.append(content)
        else:
            self.append(contents)

    def style(self) -> str:
        return """
        fieldset {
            border: 0.0625rem solid #ddd;
            padding: 1rem;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        legend {
            padding: 0 0.5rem;
            font-weight: bold;
        }
        """


class Field(Component):
    def __init__(self, **props):
        super().__init__("div", cls="form-field", **props)
        label_text = self.props.get("label")
        input_type = self.props.get("input_type", "text")
        name = self.props.get("name")
        field_id = self.props.get("id", name or f"field_{input_type}_{id(label_text)}")

        attrs = {
            k: v
            for k, v in self.props.items()
            if k not in ["label", "input_type", "name", "id"]
        }

        # Create and append label element
        label = Element("label", for_=field_id)
        label.append(label_text)
        self.append(label)

        # Create and append input element
        self.append(
            Element(
                "input", type=input_type, id=field_id, name=name or field_id, **attrs
            )
        )

    def style(self) -> str:
        return """
        .form-field {
            margin-bottom: 1rem;
            width: 100%;
            box-sizing: border-box;
        }
        .form-field label {
            display: block;
            margin-bottom: 0.5rem;
        }
        .form-field input {
            box-sizing: border-box;
            width: 100%;
            padding: 0.5rem;
            border: 0.0625rem solid #ddd;
            border-radius: 0.25rem;
        }
        """


class NavBar(Component):
    def __init__(self, **props):
        # Extract and prepare props
        direction = props.pop("direction", "row")
        cls = f"nav {props.pop('class', '')}".strip()

        # Initialize nav element
        super().__init__("nav", cls=cls, **props)

        # Create navigation list with proper orientation
        self.nav_list = Element("ul", cls=f"nav-items nav-{direction}")
        self.append(self.nav_list)

        # Add contents to nav list instead of directly to nav
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                if content is not None:
                    self.nav_list.append(content)
        elif contents is not None:
            self.nav_list.append(contents)
        self.previous_context = None  # Store previous context

    def __enter__(self):
        if self._page:
            # Store previous context
            self.previous_context = self._page._current
            # Set nav_list as current context
            self._page._current = self.nav_list
            self.nav_list._page = self._page
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            # Restore context to nav's parent
            self._page._current = self.previous_context

    def style(self) -> str:
        return """
        .nav {
            width: 100%;
            padding: 1rem;
            background: #fff;
            border-bottom: 1px solid #eee;
        }
        .nav-items {
            display: flex;
            list-style: none;
            padding: 0;
            margin: 0;
            gap: 1rem;
        }
        .nav-items.nav-column {
            flex-direction: column;
        }
        .nav-item {
            text-decoration: none;
            color: #333;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .nav-item:hover { color: #0066cc; }
        .nav-icon {
            width: 0.8rem;
            height: 1.2rem;
        }
        """


class NavItem(Component):
    def __init__(self, **props):
        # Keep special props from being passed to li element
        label = props.pop("label", "")
        url = props.pop("url", "#")
        icon = props.pop("icon", None)
        material_icon = props.pop("material_icon", None)

        # Initialize li element
        super().__init__("li", **props)

        # Build link content
        a = Element("a", href=url, cls="nav-item")

        # Handle icon (either raw icon or material icon)
        if material_icon:
            icon_component = MaterialIcon(name=material_icon, size="1.2rem")
            icon_span = Element("span", cls="nav-icon")
            icon_span.append(icon_component)
            a.append(icon_span)
        elif icon:
            icon_span = Element("span", cls="nav-icon")
            icon_span.append(icon)
            a.append(icon_span)

        label_span = Element("span")
        label_span.append(label)
        a.append(label_span)
        self.append(a)

    def style(self) -> str:
        return ""  # Uses nav styles


class Hero(Component):
    def __init__(self, **props):
        super().__init__("div", cls=f"hero {props.get('class', '')}".strip(), **props)
        # Initialize section elements
        self._title = Element("h1", cls="hero-title")
        self._subtitle = Element("p", cls="hero-subtitle")
        self._content = Element("div", cls="hero-actions")

    def title(self, text=None):
        """Set or access the hero title"""
        if text is not None:
            self._title.children = []
            self._title.append(text)
            if self._title not in self.children:
                self.append(self._title)
        return self._title

    def subtitle(self, text=None):
        """Set or access the hero subtitle"""
        if text is not None:
            self._subtitle.children = []
            self._subtitle.append(text)
            if self._subtitle not in self.children:
                self.append(self._subtitle)
        return self._subtitle

    def content(self):
        """Access the hero content section"""
        if self._content not in self.children:
            self.append(self._content)
        self._content._page = self._page
        return self._content

    def style(self) -> str:
        return """
        .hero {
            text-align: center;
            padding: 4rem 2rem;
            background: #f8f9fa;
            margin: 0;
        }
        .hero-title {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            font-size: 1.25rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .hero-actions {
            display: flex;
            gap: 1rem;
            justify-content: center;
        }
        """


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


class Grid(Component):
    def __init__(self, **props):
        cls = f"grid {props.pop('class', '')} {props.pop('cls', '')}".strip()
        cols = props.pop("cols", "auto-fit")
        min_width = props.pop("min_width", "250px")
        gap = props.pop("gap", "1rem")

        super().__init__("div", cls=cls, **props)
        self.cols = cols
        self.min_width = min_width
        self.gap = gap

    def style(self) -> str:
        return f"""
        .grid {{
            display: grid;
            grid-template-columns: repeat({self.cols}, minmax({self.min_width}, 1fr));
            gap: {self.gap};
            width: 100%;
            margin: 1rem 0;
        }}
        """


class Box(Component):
    def __init__(self, **props):
        cls = f"box {props.pop('class', '')} {props.pop('cls', '')}".strip()
        material_icon = props.pop("material_icon", None)
        icon_size = props.pop("icon_size", "1.5rem")

        super().__init__("div", cls=cls, **props)

        # Create container for content
        self.content_box = Element("div", cls="box-content")

        # Handle material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size=icon_size)
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
            gap: 1rem;
            padding: 1rem;
            background: #fff;
            border-radius: 0.25rem;
            box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
        }
        .box-icon {
            flex: 0 0 auto;
            color: #0066cc;
        }
        .box-content {
            flex: 1;
            min-width: 0;
        }
        """


class Link(Component):
    def __init__(self, **props):
        # Extract link-specific props
        text = props.pop("text", "")
        url = props.pop("url", "#")
        material_icon = props.pop("material_icon", None)
        icon_position = props.pop("icon_position", "left")  # New prop for icon position
        icon_size = props.pop("icon_size", "1.2rem")
        # Remove icon position from class since we'll handle ordering with flex-order
        cls = f"link {props.pop('class', '')} {props.pop('cls', '')}".strip()

        # Initialize with link attributes
        super().__init__("a", href=url, cls=cls, **props)

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


# Keep BASE_CSS for page-wide styles
BASE_CSS = """
:root {
    font-size: 16pt;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body { 
    max-width: 1000px;  /* Changed back to px */
    margin: 0 auto;
    padding: 0.5rem;
    font-family: system-ui, sans-serif;
    line-height: 1.5;
    overflow-x: hidden;
}

.features { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));  /* Keep px for grid */
    gap: 2rem;
    margin: 2rem 0;
}
.feature { 
    padding: 1rem; 
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
}

.container {
    width: 100%;
    max-width: 800px;  /* Changed back to px */
    margin: 0 auto;
    padding: 0.5rem;
}

[data-tooltip] {
    position: relative;
}

/* Keep pointer cursor only on interactive elements */
button[data-tooltip],
a[data-tooltip] {
    cursor: pointer;
}

[data-tooltip]:hover::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.5rem 1rem;
    background: white;
    color: #0066cc;
    border: 1px solid #e6f0ff;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    white-space: nowrap;
    box-shadow: 0 2px 4px rgba(0, 102, 204, 0.1);
    z-index: 1000;
    pointer-events: none;
    margin-bottom: 0.5rem;
}

[data-tooltip]:hover::after {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 0.5rem solid transparent;
    border-top-color: white;
    margin-bottom: -0.5rem;
    z-index: 1000;
    pointer-events: none;
}

@media (max-width: 640px) {  /* Changed back to px */
    .container { padding: 0.25rem; }
    body { padding: 0.25rem; }
}
"""
