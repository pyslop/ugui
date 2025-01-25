from .html import defaults
import warnings
from typing import List, Optional, Union
from .html import Element, TextNode, Document
from .components import get_component, _component_packs


class PageUI:
    def __init__(self, page: "Page", component_pack: str = "og"):
        self._page = page
        self._initialized_components = set()
        self._component_pack = component_pack  # Use passed component pack

    def use(self, pack_name: str) -> None:
        """Select which component pack to use"""
        self._component_pack = pack_name

    def __getattr__(self, name: str):
        """Dynamic component loading"""
        try:
            component_class = get_component(self._component_pack, name)

            def wrapper(*args, **kwargs):
                component = component_class(*args, **kwargs)
                self._init_component(component)
                return component(self._page)

            return wrapper
        except ValueError:
            raise AttributeError(f"Component {name!r} not found")

    def _init_component(self, component: "Component") -> None:
        """Initialize component CSS if not already done"""
        component_name = component.__class__.__name__
        if component_name not in self._initialized_components:
            self._page.style(component.style())
            self._initialized_components.add(component_name)


class Page:
    def __init__(
        self, minify: bool = True, style: bool | str = True, component_pack: str = "og"
    ):
        self.document = Document(minify=minify, style=style)
        self._current = self.document
        self._ui = None
        self._component_instances = {}
        self._component_pack = component_pack
        self._init_styles(style)

    def _init_styles(self, style: bool | str) -> None:
        # Initialize with base styles
        if style is True:
            # First add BASE_CSS
            from .components.base_css import BASE_CSS

            self.style(BASE_CSS)

            # Then add pack-specific base styles if any
            if self.ui._component_pack in _component_packs:
                pack_module = _component_packs[self.ui._component_pack]
                print(f"Found component pack {self.ui._component_pack!r}")
                if hasattr(pack_module, "BASE_CSS"):
                    print(f"Adding base styles for {self.ui._component_pack!r}")
                    self.style(pack_module.BASE_CSS)
            else:
                print(f"Component pack {self.ui._component_pack!r} not found")
        elif isinstance(style, str):
            self.document.link_stylesheet(style)

    @property
    def ui(self) -> PageUI:
        """Access UI components builder"""
        if self._ui is None:
            self._ui = PageUI(self, component_pack=self._component_pack)
        return self._ui

    def use(self, pack_name: str) -> None:
        """Select which component pack to use"""
        self._component_pack = pack_name
        self._ui.use(pack_name)

    def __str__(self):
        return self.document.render()

    def __getattr__(self, _name: str):
        """First try to get a component, fall back to HTML element"""
        # First check if we have a stored instance
        if _name in self._component_instances:
            return self._component_instances[_name]

        # Try to get component first
        from .components import get_component

        try:
            component_class = get_component(self.ui._component_pack, _name)

            def component_wrapper(*args, **kwargs):
                component = component_class(*args, **kwargs)
                # Initialize component CSS
                component_name = component.__class__.__name__
                if component_name not in self.ui._initialized_components:
                    self.style(component.style())
                    self.ui._initialized_components.add(component_name)
                # Add to page
                component._page = self
                self._current.append(component)
                # Store the instance
                self._component_instances[_name.lower()] = component
                return component

            return component_wrapper

        except (ValueError, ImportError):
            # Fall back to HTML element behavior
            def element_wrapper(*contents, **attrs):
                if _name.lower() in defaults.void_tags and contents:
                    warnings.warn(f"Void tag {_name!r} cannot have content")
                elem = Element(_name, **attrs)
                elem._page = self
                self._current.append(elem)
                for content in contents:
                    if elem.validate_content(content):
                        elem.append(content)
                return elem

            return element_wrapper

    def text(self, content: str) -> None:
        """Add text content as a paragraph"""
        return self.p(content)

    def raw(self, content: str) -> None:
        """Add raw unescaped text content"""
        self._current.append(TextNode(content, raw=True))

    def style(self, css: str) -> None:
        """Add CSS rules to the document"""
        self.document.styles.add(css)
