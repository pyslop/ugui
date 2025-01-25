from importlib import import_module
from typing import Dict, Type
from .og import Component

_component_packs: Dict[str, Dict[str, Type[Component]]] = {}


def register_pack(name: str, module_path: str) -> None:
    """Register a component pack by name and module path"""
    try:
        module = import_module(module_path)
        _component_packs[name] = {
            k.lower(): v
            for k, v in module.__dict__.items()
            if isinstance(v, type) and issubclass(v, Component) and v != Component
        }
    except ImportError as e:
        raise ImportError(f"Could not load component pack {name!r}: {e}")


def get_component(pack: str, name: str) -> Type[Component]:
    """Get a component class from a registered pack"""
    if pack not in _component_packs:
        raise ValueError(f"Component pack {pack!r} not found")
    if name.lower() not in _component_packs[pack]:
        raise ValueError(f"Component {name!r} not found in pack {pack!r}")
    return _component_packs[pack][name.lower()]


# Register built-in packs
register_pack("og", "ugui.components.og")
