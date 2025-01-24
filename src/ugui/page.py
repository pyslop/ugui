from .html import defaults
from typing import List, Optional


class Node:
    def __init__(self):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []

    def append(self, child: "Node") -> None:
        if isinstance(child, str):
            child = TextNode(child)
        child.parent = self
        self.children.append(child)

    def render(self) -> str:
        return "".join(child.render() for child in self.children)


class TextNode(Node):
    def __init__(self, text: str, raw: bool = False):
        super().__init__()
        self.text = text
        self.raw = raw

    def render(self) -> str:
        # For raw text, return as-is
        if self.raw:
            return self.text
        # For regular text, could add HTML escaping here if needed
        return str(self.text)


class Element(Node):
    def __init__(self, _name: str, **attrs):
        super().__init__()
        self._name = _name
        self.attrs = attrs
        self._page = None  # Reference to page for context management

    def render(self) -> str:
        attrs = "".join(
            f' {k}="{v}"' for k, v in self.attrs.items() if not isinstance(v, bool)
        )
        attrs += "".join(f" {k}" for k, v in self.attrs.items() if isinstance(v, bool))

        if self._name.lower() in defaults.void_tags:
            return f"<{self._name}{attrs}/>"

        return f"<{self._name}{attrs}>{super().render()}</{self._name}>"

    def __enter__(self):
        if self._page:
            self._page._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page and self._page._current == self:
            self._page._current = self.parent


class Document(Node):
    def __init__(self):
        super().__init__()
        self.doctype = "html"
        self.lang = "en"

    def render(self) -> str:
        return (
            f"<!DOCTYPE {self.doctype}>"
            f'<html lang="{self.lang}">'
            f"{super().render()}"
            f"</html>"
        )


class Page:
    def __init__(self):
        self.document = Document()
        self._current = self.document

    def __str__(self):
        return self.document.render()

    def __getattr__(self, _name: str):
        def tag(*contents, **attrs):
            elem = Element(_name, **attrs)
            elem._page = self  # Set page reference
            self._current.append(elem)

            # Add any contents
            for content in contents:
                elem.append(content)

            return elem

        return tag

    def text(self, content: str) -> None:
        """Add text content as a paragraph"""
        return self.p(content)

    def raw(self, content: str) -> None:
        """Add raw unescaped text content"""
        self._current.append(TextNode(content, raw=True))
