from .html import Element
from .components import Component, MaterialIcon


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


class Grid(Component):
    def __init__(self, **props):
        cls = f"grid {props.pop('class', '')} {props.pop('cls', '')}".strip()
        cols = props.pop("cols", "auto-fit")
        min_width = props.pop("min_width", "250px")
        gap = props.pop("gap", "1rem")

        super().__init__("div", cls=cls, **props)
        self.cols = cols
        self.min_width = min_width
        self.gap = gap

    def style(self) -> str:
        return f"""
        .grid {{
            display: grid;
            grid-template-columns: repeat({self.cols}, minmax({self.min_width}, 1fr));
            gap: {self.gap};
            width: 100%;
            margin: 1rem 0;
        }}
        """


class Box(Component):
    def __init__(self, **props):
        cls = f"box {props.pop('class', '')} {props.pop('cls', '')}".strip()
        material_icon = props.pop("material_icon", None)
        icon_size = props.pop("icon_size", "2.5rem")  # Increased from 1.8rem

        super().__init__("div", cls=cls, **props)

        # Create container for content
        self.content_box = Element("div", cls="box-content")

        # Handle material icon if specified
        if material_icon:
            icon = MaterialIcon(name=material_icon, size=icon_size)
            icon_wrapper = Element("div", cls="box-icon")
            icon_wrapper.append(icon)
            self.append(icon_wrapper)

        self.append(self.content_box)

    def __enter__(self):
        if self._page:
            self._page._current = self.content_box
            self.content_box._page = self._page
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            self._page._current = self.parent

    def style(self) -> str:
        return """
        .box {
            display: flex;
            align-items: flex-start;
            gap: 1.5rem;  /* Increased from 1rem */
            padding: 1.5rem;  /* Increased from 1rem */
            background: var(--color-bg);
            border-radius: 0.5rem;  /* Increased from 0.25rem */
            box-shadow: 0 0 1rem var(--color-shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .box:hover {
            transform: translateY(-2px);
            box-shadow: 0 0.5rem 2rem var(--color-shadow-hover);
        }
        .box-icon {
            flex: 0 0 auto;
            color: var(--color-primary);
            transition: transform 0.2s ease;
        }
        .box:hover .box-icon {
            transform: scale(1.1);
            color: var(--color-primary-hover);
        }
        .box-content {
            flex: 1;
            min-width: 0;
        }
        .box-content h3 {
            margin-bottom: 0.5rem;
            color: var(--color-primary);
        }
        """


class Link(Component):
    def __init__(self, **props):
        # Extract link-specific props
        text = props.pop("text", "")
        url = props.pop("url", "#")
        material_icon = props.pop("material_icon", None)
        icon_position = props.pop("icon_position", "left")  # New prop for icon position
        icon_size = props.pop("icon_size", "1.8rem")
        # Remove icon position from class since we'll handle ordering with flex-order
        cls = f"link {props.pop('class', '')} {props.pop('cls', '')}".strip()

        # Initialize with link attributes
        super().__init__("a", href=url, cls=cls, **props)

        # Add text content first in a span
        text_span = Element("span", cls="link-text")
        text_span.append(text)
        self.append(text_span)

        # Add icon with proper ordering class
        if material_icon:
            icon_span = MaterialIcon(
                name=material_icon,
                size=icon_size,
                cls=f"link-icon link-icon-{icon_position}",
            )
            self.append(icon_span)

    def style(self) -> str:
        return """
        .link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #0066cc;
            text-decoration: none;
            white-space: nowrap;
        }
        .link:hover {
            text-decoration: underline;
        }
        .link .link-icon {
            display: inline-flex;
            color: inherit;
            opacity: 0.8;
        }
        .link:hover .link-icon {
            opacity: 1;
        }
        .link .link-icon-left {
            order: -1;  /* Place before text */
        }
        .link .link-icon-right {
            order: 1;   /* Place after text */
        }
        .link .link-text {
            order: 0;   /* Keep text in middle */
            display: inline-block;
            line-height: 1;
        }
        """


# Keep BASE_CSS for page-wide styles
BASE_CSS = """
:root {
    /* Base theme */
    --font-size: 16pt;
    --font-family: system-ui, sans-serif;
    
    /* Colors - Light theme defaults */
    --color-primary: #0066cc;
    --color-primary-hover: #0052a3;
    --color-primary-bg: rgba(0, 102, 204, 0.1);
    --color-primary-bg-hover: rgba(0, 102, 204, 0.2);
    
    --color-text: #333333;
    --color-text-secondary: #666666;
    
    --color-bg: #ffffff;
    --color-bg-subtle: #f8f9fa;
    --color-bg-hover: #f0f0f0;
    
    --color-border: #dddddd;
    --color-shadow: rgba(0, 0, 0, 0.1);
    --color-shadow-hover: rgba(0, 0, 0, 0.15);

    /* Tooltip colors */
    --tooltip-bg: white;
    --tooltip-border: #e6f0ff;
}

@media (prefers-color-scheme: dark) {
    :root {
        /* Colors - Dark theme */
        --color-primary: #66b3ff;
        --color-primary-hover: #99ccff;
        --color-primary-bg: rgba(102, 179, 255, 0.1);
        --color-primary-bg-hover: rgba(102, 179, 255, 0.2);
        
        --color-text: #e0e0e0;
        --color-text-secondary: #a0a0a0;
        
        --color-bg: #1a1a1a;
        --color-bg-subtle: #2a2a2a;
        --color-bg-hover: #333333;
        
        --color-border: #404040;
        --color-shadow: rgba(0, 0, 0, 0.3);
        --color-shadow-hover: rgba(0, 0, 0, 0.4);

        /* Tooltip colors */
        --tooltip-bg: #2a2a2a;
        --tooltip-border: #404040;
    }
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body { 
    max-width: 1000px;  /* Changed back to px */
    margin: 0 auto;
    padding: 0.5rem;
    font-family: var(--font-family);
    font-size: var(--font-size);
    line-height: 1.5;
    overflow-x: hidden;
    background: var(--color-bg);
    color: var(--color-text);
}

.features { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));  /* Keep px for grid */
    gap: 2rem;
    margin: 2rem 0;
}
.feature { 
    padding: 1rem; 
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
}

.container {
    width: 100%;
    max-width: 800px;  /* Changed back to px */
    margin: 0 auto;
    padding: 0.5rem;
}

[data-tooltip] {
    position: relative;
}

/* Keep pointer cursor only on interactive elements */
button[data-tooltip],
a[data-tooltip] {
    cursor: pointer;
}

[data-tooltip]:hover::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.5rem 1rem;
    background: var(--tooltip-bg);
    color: var(--color-primary);
    border: 1px solid var(--tooltip-border);
    border-radius: 0.25rem;
    font-size: 0.875rem;
    white-space: nowrap;
    box-shadow: 0 2px 4px var(--color-shadow);
    z-index: 1000;
    pointer-events: none;
    margin-bottom: 0.5rem;
}

[data-tooltip]:hover::after {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 0.5rem solid transparent;
    border-top-color: var(--tooltip-bg);
    margin-bottom: -0.5rem;
    z-index: 1000;
    pointer-events: none;
}

@media (max-width: 640px) {  /* Changed back to px */
    .container { padding: 0.25rem; }
    body { padding: 0.25rem; }
}
"""
