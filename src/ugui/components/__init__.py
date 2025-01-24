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

    def __call__(self, page: Any) -> Any:
        """Make components callable for page context"""
        self._page = page
        if hasattr(page, "_current"):
            self.parent = page._current
            page._current.append(self)
        return self


from ugui.components.material_icon import MaterialIcon
from ugui.components.box import Box
from ugui.components.button import Button
from ugui.components.card import Card
from ugui.components.form import Field, Fieldset, Form
from ugui.components.grid import Grid
from ugui.components.hero import Hero
from ugui.components.navbar import NavBar, NavItem


__all__ = [
    "Box",
    "Button",
    "Component",
    "Card",
    "Field",
    "Fieldset",
    "Form",
    "Grid",
    "Hero",
    "MaterialIcon",
    "NavBar",
    "NavItem",
]
