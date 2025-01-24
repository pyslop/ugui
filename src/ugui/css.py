class CSSRegistry:
    def __init__(self):
        self._styles = set()

    def add(self, css: str) -> None:
        """Add CSS rules to the registry"""
        self._styles.add(css.strip())

    def render(self) -> str:
        """Render all registered CSS rules"""
        return "\n".join(sorted(self._styles))
