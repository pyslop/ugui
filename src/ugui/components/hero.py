from . import Component, Element


class Hero(Component):
    def __init__(self, **props):
        super().__init__("div", cls=f"hero {props.get('class', '')}".strip(), **props)
        # Initialize section elements
        self._title = Element("h1", cls="hero-title")
        self._subtitle = Element("p", cls="hero-subtitle")
        self._content = Element("div", cls="hero-actions")

    def title(self, text=None):
        """Set or access the hero title"""
        if text is not None:
            self._title.children = []
            self._title.append(text)
            if self._title not in self.children:
                self.append(self._title)
        return self._title

    def subtitle(self, text=None):
        """Set or access the hero subtitle"""
        if text is not None:
            self._subtitle.children = []
            self._subtitle.append(text)
            if self._subtitle not in self.children:
                self.append(self._subtitle)
        return self._subtitle

    def content(self):
        """Access the hero content section"""
        if self._content not in self.children:
            self.append(self._content)
        self._content._page = self._page
        return self._content

    def style(self) -> str:
        return """
        .hero {
            text-align: center;
            padding: 4rem 2rem;
            background: var(--color-bg-subtle);
            margin: 0;
        }
        .hero-title {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--color-text);
        }
        .hero-subtitle {
            font-size: 1.25rem;
            color: var(--color-text-secondary);
            margin-bottom: 2rem;
        }
        .hero-actions {
            display: flex;
            gap: 1rem;
            justify-content: center;
        }
        """
