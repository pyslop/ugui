from .html import defaults
import warnings
from typing import List, Optional, Union
from .components import CARD_CSS, FORM_CSS, BUTTON_CSS, BASE_CSS
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
        self.styles = CSSRegistry()

    def collect_styles(self) -> str:
        """Collect all styles and render them"""
        if self.styles._styles:
            return f"<style>{self.styles.render()}</style>"
        return ""

    def render(self) -> str:
        html = f"<!DOCTYPE {self.doctype}><html lang='{self.lang}'>"

        # Find head element or create one
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

        # Render final HTML
        return html + super().render() + "</html>"


class PageUI:
    def __init__(self, page: "Page"):
        self._page = page
        self._initialized_components = set()

    def _init_component(self, name: str, css: str) -> None:
        """Initialize component CSS if not already done"""
        if name not in self._initialized_components:
            self._page.style(css)
            self._initialized_components.add(name)

    def card(self, *contents, title=None, footer=None, cls="card", **attrs):
        """Create a card component with optional title and footer"""
        self._init_component("card", CARD_CSS)
        attrs["class"] = f"{cls} {attrs.get('class', '')}"
        with self._page.div(**attrs) as card:
            if title:
                self._page.div(title, cls="card-header")
            with self._page.div(cls="card-body"):
                for content in contents:
                    self._page.append(content)
            if footer:
                self._page.div(footer, cls="card-footer")
        return card

    def form(self, *contents, action="#", method="post", **attrs):
        """Create a form with specified action and method"""
        self._init_component("form", FORM_CSS)
        attrs.update(action=action, method=method)
        with self._page.form(**attrs) as form:
            for content in contents:
                self._page.append(content)
        return form

    def fieldset(self, *contents, legend=None, **attrs):
        """Create a fieldset with optional legend"""
        with self._page.fieldset(**attrs) as fs:
            if legend:
                self._page.legend(legend)
            for content in contents:
                self._page.append(content)
        return fs

    def field(self, label, input_type="text", name=None, **attrs):
        """Create a labeled form field"""
        field_id = attrs.pop("id", name or f"field_{input_type}_{id(label)}")
        with self._page.div(cls="form-field") as container:
            self._page.label(label, for_=field_id)
            self._page.input(
                type=input_type, id=field_id, name=name or field_id, **attrs
            )
        return container

    def button(self, text, **attrs):
        """Create a styled button"""
        self._init_component("button", BUTTON_CSS)
        cls = f"btn {attrs.pop('cls', '')}"
        return self._page.button(text, cls=cls.strip(), **attrs)


class Page:
    def __init__(self):
        self.document = Document()
        self._current = self.document
        self._ui = None
        # Initialize with base styles
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
