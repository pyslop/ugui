from . import Component, MaterialIcon
from ugui.html import Element


class Card(Component):
    def __init__(self, **props):
        props["class"] = "card"
        super().__init__("div", **props)

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
            icon = MaterialIcon(
                name=material_icon, size="1.8rem", **props
            )  # Changed from 1.4rem
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
            icon = MaterialIcon(
                name=material_icon, size="1.8rem", **props
            )  # Changed from 1.4rem
            self._footer.children.insert(0, icon)

        return self._footer

    def style(self) -> str:
        return """
        .card {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            border: 0.0625rem solid var(--color-border);
            border-radius: 0.25rem;
            margin: 1rem 0;
            overflow: hidden;
            background: var(--color-bg);
        }
        .card-header {
            padding: 1rem;
            border-bottom: 0.0625rem solid var(--color-border);
            background: var(--color-bg-subtle);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card-header .material-icon {
            color: var(--color-primary);
            opacity: 0.9;
            transition: transform 0.2s ease;
            height: 1.8rem;  /* Changed from 1.4rem */
        }
        .card-header:hover .material-icon {
            transform: scale(1.1);
            opacity: 1;
        }
        .card-body { padding: 1rem; }
        .card-footer {
            padding: 1rem;
            border-top: 0.0625rem solid var(--color-border);
            background: var(--color-bg-subtle);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .card-footer .material-icon {
            color: var(--color-primary);
            opacity: 0.9;
            transition: transform 0.2s ease;
            height: 1.8rem;  /* Changed from 1.4rem */
        }
        .card-footer:hover .material-icon {
            transform: scale(1.1);
            opacity: 1;
        }
        """
