from typing import List, Optional, Union
import warnings
from .css import CSSRegistry


class defaults:
    remove_first_underscore = True
    replace_single_underscore = False
    replace_double_underscore = True
    replace_className = True
    replace_cls = True
    # https://html.spec.whatwg.org/multipage/syntax.html#the-doctype
    doctypes = {"html"}
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element
    tags = {
        "html",
        "head",
        "link",
        "meta",
        "style",
        "title",
        "body",
        "address",
        "article",
        "aside",
        "footer",
        "header",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hgroup",
        "nav",
        "section",
        "blockquote",
        "dd",
        "dl",
        "dt",
        "div",
        "figcaption",
        "figure",
        "hr",
        "ul",
        "ol",
        "li",
        "main",
        "p",
        "pre",
        "a",
        "abbr",
        "b",
        "bdi",
        "bdo",
        "br",
        "cite",
        "code",
        "data",
        "dfn",
        "em",
        "i",
        "kbd",
        "mark",
        "q",
        "rp",
        "rt",
        "rtc",
        "ruby",
        "s",
        "samp",
        "small",
        "span",
        "strong",
        "sub",
        "sup",
        "time",
        "u",
        "var",
        "wbr",
        "area",
        "audio",
        "img",
        "map",
        "track",
        "video",
        "embed",
        "iframe",
        "object",
        "param",
        "picture",
        "source",
        "canvas",
        "noscript",
        "script",
        "del",
        "ins",
        "caption",
        "col",
        "colgroup",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "tr",
        "button",
        "datalist",
        "fieldset",
        "form",
        "input",
        "label",
        "legend",
        "meter",
        "optgroup",
        "option",
        "output",
        "progress",
        "select",
        "textarea",
        "details",
        "dialog",
        "menu",
        "summary",
        "slot",
        "template",
    }
    void_tags = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
    deprecated_tags = {
        "acronym",
        "applet",
        "basefont",
        "bgsound",
        "big",
        "blink",
        "center",
        "command",
        "content",
        "dir",
        "element",
        "font",
        "frame",
        "frameset",
        "image",
        "isindex",
        "keygen",
        "listing",
        "marquee",
        "menuitem",
        "multicol",
        "nextid",
        "nobr",
        "noembed",
        "noframes",
        "plaintext",
        "shadow",
        "spacer",
        "strike",
        "tt",
        "xmp",
    }


class Node:
    def __init__(self):
        self.parent: Optional[Node] = None
        self.children: List[Node] = []

    def append(self, child: "Node") -> "Node":
        if isinstance(child, str):
            child = TextNode(child)
        child.parent = self
        self.children.append(child)
        return self

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
        if minify:
            return text.strip()

        text = text.strip()
        if not text:
            return ""
        return " " * indent + text + "\n"


class Element(Node):
    def __init__(self, _name: str, **attrs):
        super().__init__()
        if defaults.remove_first_underscore and _name.startswith("_"):
            _name = _name[1:]
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
            elif k.endswith("_"):
                k = k[:-1]
            elif "__" in k:
                k = k.replace("__", "-")
            elif "_" in k:
                k = k.replace("_", "-")
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

        # Basic indentation rules
        content = super().render(indent + indent_size, indent_size, minify)
        if not content.strip():
            return f"{spaces}<{self._name}{attrs}></{self._name}>\n"

        content = content.rstrip()
        return f"{spaces}<{self._name}{attrs}>\n{content}\n{spaces}</{self._name}>\n"

    def __enter__(self):
        if self._page:
            self._page._current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page and self._page._current == self:
            self._page._current = self.parent


class Document(Node):
    def __init__(self, minify=True, style: bool | str = True, indent_size: int = 2):
        super().__init__()
        self.doctype = "html"
        self.lang = "en"
        self.styles = CSSRegistry()
        self.minify = minify
        self.styles_enabled = style
        self.indent_size = indent_size
        self._link_stylesheets = []

        # Define default meta tags
        self.default_meta = [
            # Removed from list since we'll handle charset separately
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
        # Keep charset separate to ensure it's always first
        self.charset_meta = {"charset": "utf-8"}

    def link_stylesheet(self, href: str) -> None:
        """Add a link to an external stylesheet"""
        self._link_stylesheets.append(href)

    def collect_styles(self) -> str:
        """Collect all styles and render them"""
        if not self.styles_enabled or not self.styles:
            print(">>> self.styles_enabled", self.styles_enabled)
            return ""
        if not self.styles._styles:
            return ""
        styles = self.styles.render(minify=self.minify)
        if self.minify:
            return f"<style>{styles}</style>"

        # Indent the style tag content properly
        indent = " " * self.indent_size
        style_content = "\n".join(
            f"{indent}{line}" for line in styles.split("\n") if line.strip()
        )
        return f"<style>\n{style_content}\n{indent+indent}</style>"

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

        # Get ordered head elements
        charset_tag = None
        meta_tags = []
        title_tag = None
        other_tags = []

        # Group head elements by type
        for child in head.children:
            if isinstance(child, Element):
                if child._name == "meta" and "charset" in child.attrs:
                    charset_tag = child
                elif child._name == "meta":
                    meta_tags.append(child)
                elif child._name == "title":
                    title_tag = child
                else:
                    other_tags.append(child)

        # Clear head contents for reordering
        head.children = []

        # Always add charset meta first
        if not charset_tag:
            charset_tag = Element("meta", **self.charset_meta)
        head.children.append(charset_tag)

        # Add remaining default meta tags if they don't exist
        existing_meta = {tuple(sorted(meta.attrs.items())) for meta in meta_tags}
        for meta_attrs in self.default_meta:
            meta_key = tuple(sorted(meta_attrs.items()))
            if meta_key not in existing_meta:
                meta_tags.append(Element("meta", **meta_attrs))

        # Add other meta tags
        head.children.extend(meta_tags)

        # Rest of the head content
        if title_tag:
            head.children.append(title_tag)

        # Add styles
        styles = self.collect_styles()
        if styles:
            head.children.append(TextNode(styles, raw=True))

        # Add external stylesheets
        for stylesheet in self._link_stylesheets:
            head.children.append(Element("link", rel="stylesheet", href=stylesheet))

        head.children.extend(other_tags)

        if self.minify:
            html = f"<!DOCTYPE {self.doctype}><html lang='{self.lang}'>"
            return html + super().render(0, 0, True) + "</html>"

        html = f"<!DOCTYPE {self.doctype}>\n<html lang='{self.lang}'>\n"
        content = super().render(self.indent_size, self.indent_size, False)
        return html + content + "</html>\n"
