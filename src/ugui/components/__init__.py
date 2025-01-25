from importlib import import_module
from abc import abstractmethod
from typing import Any, Dict, Type
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


_component_packs: Dict[str, Any] = {}


def register_pack(name: str, module_path: str) -> None:
    """Register a component pack by name and module path"""
    try:
        module = import_module(module_path)
        # Store the entire module rather than just components
        _component_packs[name] = module
    except ImportError as e:
        raise ImportError(f"Could not load component pack {name!r}: {e}")


def get_component(pack: str, name: str) -> Type[Component]:
    """Get a component class from a registered pack"""
    if pack not in _component_packs:
        raise ValueError(f"Component pack {pack!r} not found")
    module = _component_packs[pack]
    for k, v in module.__dict__.items():
        if (
            k.lower() == name.lower()
            and isinstance(v, type)
            and issubclass(v, Component)
        ):
            return v
    raise ValueError(f"Component {name!r} not found in pack {pack!r}")


# Register built-in packs
register_pack("og", "ugui.components.og")
register_pack("plain", "ugui.components.plain")
