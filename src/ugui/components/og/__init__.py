from abc import abstractmethod
from typing import Any
from ugui.html import Element


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

    def __call__(self, page: Any = None, *args, **kwargs) -> Any:
        """Make components callable for page context"""
        # If first arg is page, it's being used in a with statement
        if page is not None and hasattr(page, "_current"):
            self._page = page
            self.parent = page._current
            page._current.append(self)
            return self
        # Otherwise, treat all args as component init args
        if args or kwargs:
            return self.__class__(*args, **kwargs)(page)
        return self


from .base_css import BASE_CSS
from .material_icon import MaterialIcon
from .box import Box
from .button import Button
from .card import Card
from .form import Form, Field, Fieldset
from .grid import Grid
from .hero import Hero
from .link import Link
from .navbar import NavBar, NavItem


__all__ = [
    "BASE_CSS",
    "Box",
    "Button",
    "Component",
    "Card",
    "Field",
    "Fieldset",
    "Form",
    "Grid",
    "Hero",
    "Link",
    "MaterialIcon",
    "NavBar",
    "NavItem",
]
