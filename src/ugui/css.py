import re


class CSSRegistry:
    # Priority order for CSS selectors
    SELECTOR_PRIORITIES = {
        # Global imports and resets (0-9)
        "@charset": 0,
        "@import": 0,
        ":root": 1,
        "html": 2,
        "body": 3,
        "*": 4,
        # Media and animation rules (10-19)
        "@media": 10,
        "@supports": 11,
        "@keyframes": 12,
        "@font-face": 13,
        # Global theme variables and utilities (20-29)
        ":host": 20,
        "[data-theme]": 21,
        ".theme-": 22,
        ".dark": 22,
        ".light": 22,
        # Global states (30-39)
        ":focus-visible": 30,
        ":focus": 31,
        ":hover": 32,
        ":active": 33,
        # Global utilities (40-49)
        ".container": 40,
        ".sr-only": 41,
        ".visually-hidden": 41,
        ".hidden": 42,
        ".clearfix": 43,
    }

    def __init__(self):
        self._styles = set()

    def add(self, css: str) -> None:
        """Add CSS rules to the registry"""
        self._styles.add(css.strip())

    def _get_rule_priority(self, rule: str) -> int:
        """Get the priority of a CSS rule based on its selector"""
        rule = rule.strip()
        for selector, priority in self.SELECTOR_PRIORITIES.items():
            if rule.startswith(selector):
                return priority
        return 100  # Regular CSS rules get higher priority

    def render(self, minify: bool = False) -> str:
        """Render all registered CSS rules

        Args:
            minify: If True, removes unnecessary whitespace from the output
        """
        # Sort rules by priority
        sorted_rules = sorted(self._styles, key=self._get_rule_priority)

        if minify:
            css = "\n".join(sorted_rules)
            css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
            css = re.sub(r"\s+", " ", css)
            return css.strip()

        return "\n".join(rule.strip() for rule in sorted_rules)
