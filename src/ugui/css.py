import re


class CSSRegistry:
    def __init__(self):
        self._styles = set()

    def add(self, css: str) -> None:
        """Add CSS rules to the registry"""
        self._styles.add(css.strip())

    def render(self, minify: bool = False) -> str:
        """Render all registered CSS rules

        Args:
            minify: If True, removes unnecessary whitespace from the output
        """
        if minify:
            css = "\n".join(sorted(self._styles))
            css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
            css = re.sub(r"\s+", " ", css)
            return css.strip()

        return "\n".join(sorted(rule.strip() for rule in self._styles))
