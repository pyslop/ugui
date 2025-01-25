from .html import defaults
import warnings
from typing import List, Optional, Union
from .components.base_css import BASE_CSS
from .components import (
    Box,
    Button,
    Card,
    Component,
    Fieldset,
    Field,
    Form,
    Grid,
    Hero,
    Link,
    MaterialIcon,
    NavBar,
    NavItem,
)
from .html import Element, TextNode, Document


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

    def navbar(self, *contents, **kwargs):
        """Create a navigation component"""
        component = NavBar(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def nav_item(self, label, url="#", icon=None, material_icon=None, icon_color=None):
        """Create a navigation item"""
        component = NavItem(
            label=label,
            url=url,
            icon=icon,
            material_icon=material_icon,
            icon_color=icon_color,
        )
        self._init_component(component)
        if hasattr(self._page, "_current") and self._page._current._name == "ul":
            # If we're in a navbar context, append directly to current ul
            self._page._current.append(component)
            return component
        return component(self._page)

    def hero(self, title=None, subtitle=None, *contents, **kwargs):
        """Create a hero component"""
        props = {"title": title, "subtitle": subtitle, "contents": contents, **kwargs}
        component = Hero(**props)
        self._init_component(component)
        return component(self._page)

    def material_icon(
        self, name: str, size: str = "24px", color: str = "currentColor", **props
    ):
        """Create a material icon component"""
        component = MaterialIcon(name=name, size=size, color=color, **props)
        self._init_component(component)
        return component(self._page)

    def grid(self, *contents, **kwargs):
        """Create a grid component"""
        component = Grid(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def box(self, *contents, **kwargs):
        """Create a box component"""
        component = Box(contents=contents, **kwargs)
        self._init_component(component)
        return component(self._page)

    def link(self, text, url="#", material_icon=None, **kwargs):
        """Create a link component"""
        component = Link(text=text, url=url, material_icon=material_icon, **kwargs)
        self._init_component(component)
        return component(self._page)


class Page:
    def __init__(self, minify: bool = True, style: bool | str = True):
        self.document = Document(minify=minify, style=style)
        self._current = self.document
        self._ui = None
        # Initialize with base styles after minify is set
        if style is True:
            self.style(BASE_CSS)
        elif isinstance(style, str):
            self.document.link_stylesheet(style)

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
