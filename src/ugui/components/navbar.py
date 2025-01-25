from . import Component, Element
from .material_icon import MaterialIcon


class NavBar(Component):
    def __init__(self, **props):
        # Extract and prepare props
        direction = props.pop("direction", "row")
        props["class"] = "nav"
        # Initialize nav element
        super().__init__("nav", **props)

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
            background: var(--color-bg);
            border-bottom: 0.0625rem solid var(--color-border);
        }
        .nav-items {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
            list-style: none;
            padding: 0;
            margin: 0;
            gap: 1rem;
        }
        .nav-items.nav-column {
            flex-direction: column;
        }
        @media (max-width: 768px) {
            .nav-items {
                flex-direction: column;
            }
            .nav-item {
                width: 100%;
            }
        }
        .nav-item {
            text-decoration: none;
            color: var(--color-text);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.2s ease;
            padding: 0.5rem;
        }
        .nav-item:hover { 
            color: var(--color-primary); 
            background: var(--color-bg-secondary);
            border-radius: 0.25rem;
        }
        .nav-item .material-icon {
            opacity: 0.8;
            transition: transform 0.2s ease, opacity 0.2s ease;
            display: inline-flex;
            align-items: center;
        }
        .nav-item:hover .material-icon {
            opacity: 1;
            transform: scale(1.1);
        }
        .nav-icon {
            display: inline-flex;
            width: 1.4rem;
            height: 1.4rem;
        }
        """


class NavItem(Component):
    def __init__(self, **props):
        # Keep special props from being passed to li element
        label = props.pop("label", "")
        url = props.pop("url", "#")
        icon = props.pop("icon", None)
        material_icon = props.pop("material_icon", None)
        icon_color = props.pop("icon_color", None)

        # Initialize li element
        super().__init__("li", **props)

        # Build link content
        a = Element("a", href=url, cls="nav-item")

        # Handle icon (either raw icon or material icon)
        if material_icon:
            icon_component = MaterialIcon(
                name=material_icon, size="1.4rem", color=icon_color
            )
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
