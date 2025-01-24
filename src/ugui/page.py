from .html import defaults
import warnings
from typing import List, Optional, Union
from .component import BASE_CSS, Card, Form, Button, Fieldset, Field
from .css import CSSRegistry


class Node:
    def __init__(self):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []

    def append(self, child: "Node") -> None:
        if isinstance(child, str):
            child = TextNode(child)
        child.parent = self
        self.children.append(child)

    def render(
        self, indent: int = 0, indent_size: int = 2, minify: bool = False
    ) -> str:
        parts = []
        for child in self.children:
            parts.append(child.render(indent, indent_size, minify))
        return "".join(parts)


class TextNode(Node):
    def __init__(self, text: str, raw: bool = False):
        super().__init__()
        self.text = text
        self.raw = raw

    def render(
        self, indent: int = 0, indent_size: int = 2, minify: bool = False
    ) -> str:
        text = self.text if self.raw else str(self.text)
        if not text.strip() or minify:
            return text
        return " " * indent + text


class Element(Node):
    def __init__(self, _name: str, **attrs):
        super().__init__()
        self._name = _name.lower()

        # Validate tag
        if self._name in defaults.deprecated_tags:
            warnings.warn(
                f"The {self._name!r} tag is deprecated. "
                "See: https://developer.mozilla.org/en-US/docs/Web/HTML/Element"
            )
        if self._name not in defaults.tags and self._name not in defaults.void_tags:
            warnings.warn(f"Unknown tag {self._name!r}")

        # Fix attribute names
        self.attrs = {}
        for k, v in attrs.items():
            if k == "cls" or k == "className":
                k = "class"
            elif "__" in k:
                k = k.replace("__", "-")
            self.attrs[k] = v

        self._page = None

        if _name == "style":
            # Get document root
            root = self
            while root.parent:
                root = root.parent
            if isinstance(root, Document):
                root.styles.add(attrs.get("content", ""))

    def validate_content(self, content: any) -> bool:
        """Validate content can be added to this element"""
        if content is None:
            return False
        if isinstance(content, (str, Element, Document, TextNode)):  # Added TextNode
            return True
        raise TypeError(
            f"Invalid content for {self._name!r}: {content!r}, "
            "expected str, Element, Document or TextNode"
        )

    def append(self, child: Union[Node, str]) -> None:
        if isinstance(child, str) and self._name == "style":
            # Add style content to document styles
            root = self
            while root.parent:
                root = root.parent
            if isinstance(root, Document):
                root.styles.add(child)
        else:
            super().append(child)

    def render(
        self, indent: int = 0, indent_size: int = 2, minify: bool = False
    ) -> str:
        attrs = "".join(
            f' {k}="{v}"' for k, v in self.attrs.items() if not isinstance(v, bool)
        )
        attrs += "".join(f" {k}" for k, v in self.attrs.items() if isinstance(v, bool))

        if minify:
            if self._name.lower() in defaults.void_tags:
                return f"<{self._name}{attrs}/>"
            content = super().render(0, 0, True)
            return f"<{self._name}{attrs}>{content}</{self._name}>"

        spaces = " " * indent
        if self._name.lower() in defaults.void_tags:
            return f"{spaces}<{self._name}{attrs}/>\n"

        content = super().render(indent + indent_size, indent_size, minify)
        if not content.strip():
            return f"{spaces}<{self._name}{attrs}></{self._name}>\n"

        return f"{spaces}<{self._name}{attrs}>\n{content}{spaces}</{self._name}>\n"

    def __enter__(self):
        if self._page:
            self._page._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page and self._page._current == self:
            self._page._current = self.parent


class Document(Node):
    def __init__(self, minify=True, indent_size: int = 2):
        super().__init__()
        self.doctype = "html"
        self.lang = "en"
        self.styles = CSSRegistry()
        self.minify = minify
        self.indent_size = indent_size

    def collect_styles(self) -> str:
        """Collect all styles and render them"""
        if not self.styles._styles:
            return ""
        styles = self.styles.render(minify=self.minify)
        if self.minify:
            return f"<style>{styles}</style>"
        return f"<style>\n  {styles}\n</style>"

    def render(self) -> str:
        # Find or create head element
        head = next(
            (
                child
                for child in self.children
                if isinstance(child, Element) and child._name == "head"
            ),
            None,
        )
        if not head:
            head = Element("head")
            self.children.insert(0, head)

        # Insert styles at start of head
        styles = self.collect_styles()
        if styles:
            head.children.insert(0, TextNode(styles, raw=True))

        if self.minify:
            html = f"<!DOCTYPE {self.doctype}><html lang='{self.lang}'>"
            return html + super().render(0, 0, True) + "</html>"

        html = f"<!DOCTYPE {self.doctype}>\n<html lang='{self.lang}'>\n"
        content = super().render(self.indent_size, self.indent_size, False)
        return html + content + "</html>\n"


class PageUI:
    def __init__(self, page: "Page"):
        self._page = page
        self._initialized_components = set()

    def _init_component(self, component: "Component") -> None:
        """Initialize component CSS if not already done"""
        component_name = component.__class__.__name__
        if component_name not in self._initialized_components:
            self._page.style(component.style())
            self._initialized_components.add(component_name)

    def card(self, *contents, **kwargs):
        """Create a card component"""
        component = Card(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def form(self, *contents, **kwargs):
        """Create a form component"""
        component = Form(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def button(self, text, **kwargs):
        """Create a button component"""
        component = Button(text=text, **kwargs)
        self._init_component(component)
        return component(self._page)

    def fieldset(self, *contents, **kwargs):
        """Create a fieldset component"""
        component = Fieldset(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def field(self, label, **kwargs):
        """Create a form field component"""
        component = Field(label=label, **kwargs)
        self._init_component(component)
        return component(self._page)

    # Fieldset and field methods can be converted similarly


class Page:
    def __init__(self, minify: bool = True):
        self.document = Document(minify=minify)  # Pass minify directly
        self._current = self.document
        self._ui = None
        # Initialize with base styles after minify is set
        self.style(BASE_CSS)

    @property
    def ui(self) -> PageUI:
        """Access UI components builder"""
        if self._ui is None:
            self._ui = PageUI(self)
        return self._ui

    def __str__(self):
        return self.document.render()

    def __getattr__(self, _name: str):
        def tag(*contents, **attrs):
            # Create proper element type based on tag name
            if _name.lower() in defaults.void_tags:
                # Void elements can't have content
                if contents:
                    warnings.warn(f"Void tag {_name!r} cannot have content")
                elem = Element(_name, **attrs)
            else:
                elem = Element(_name, **attrs)

            elem._page = self
            self._current.append(elem)

            # Add validated contents

            for content in contents:
                if elem.validate_content(content):
                    elem.append(content)

            return elem

        return tag

    def text(self, content: str) -> None:
        """Add text content as a paragraph"""
        return self.p(content)

    def raw(self, content: str) -> None:
        """Add raw unescaped text content"""
        self._current.append(TextNode(content, raw=True))

    def style(self, css: str) -> None:
        """Add CSS rules to the document"""
        self.document.styles.add(css)
