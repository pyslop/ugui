from abc import ABC, abstractmethod
from typing import Any, Optional
from .html import Element


class Component(Element):
    def __init__(self, _name: str = "div", **props):
        super().__init__(
            _name, **{k: v for k, v in props.items() if k not in ["contents"]}
        )
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


from .component import Component


class Card(Component):
    def __init__(self, **props):
        super().__init__("div", cls=f"card {props.get('class', '')}".strip(), **props)
        if self.props.get("title"):
            header = Element("div", cls="card-header")
            header.append(self.props["title"])
            self.append(header)

        body = Element("div", cls="card-body")
        contents = self.props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                body.append(content)
        else:
            body.append(contents)
        self.append(body)

        if self.props.get("footer"):
            footer = Element("div", cls="card-footer")
            footer.append(self.props["footer"])
            self.append(footer)

    def style(self) -> str:
        return """
        .card {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 1rem 0;
            overflow: hidden;
        }
        .card-header {
            padding: 1rem;
            border-bottom: 1px solid #ddd;
            background: #f8f9fa;
        }
        .card-body { padding: 1rem; }
        .card-footer {
            padding: 1rem;
            border-top: 1px solid #ddd;
            background: #f8f9fa;
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

        # Initialize with combined class and remaining props
        super().__init__("button", cls=cls, **props)

        if text:
            self.append(text)

    def style(self) -> str:
        return """
        .btn {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 0.5rem;
        }
        .btn.secondary {
            background: transparent;
            border: 1px solid #0066cc;
            color: #0066cc;
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
            border: 1px solid #ddd;
            padding: 1rem;
            border-radius: 4px;
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
            border: 1px solid #ddd;
            border-radius: 4px;
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
            width: 1em;
            height: 1em;
        }
        """


class NavItem(Component):
    def __init__(self, **props):
        # Keep label/url/icon from being passed to li element
        label = props.pop("label", "")
        url = props.pop("url", "#")
        icon = props.pop("icon", None)

        # Initialize li element
        super().__init__("li", **props)

        # Build link content
        a = Element("a", href=url, cls="nav-item")
        if icon:
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
        super().__init__("div", cls="hero", **props)
        if self.props.get("title"):
            h1 = Element("h1", cls="hero-title")
            h1.append(self.props["title"])
            self.append(h1)

        if self.props.get("subtitle"):
            p = Element("p", cls="hero-subtitle")
            p.append(self.props["subtitle"])
            self.append(p)

        contents = self.props.get("contents", [])
        if contents:
            actions = Element("div", cls="hero-actions")
            if isinstance(contents, (list, tuple)):
                for content in contents:
                    actions.append(content)
            else:
                actions.append(contents)
            self.append(actions)

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


# Keep BASE_CSS for page-wide styles
BASE_CSS = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body { 
    max-width: 800px; 
    margin: 0 auto;
    padding: 0.5rem;
    font-family: system-ui, sans-serif;
    line-height: 1.5;
    overflow-x: hidden;
}

a { color: #0066cc; }

.features { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}
.feature { padding: 1rem; }

.container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 0.5rem;
}

@media (max-width: 640px) {
    .container { padding: 0.25rem; }
    body { padding: 0.25rem; }
}
"""
