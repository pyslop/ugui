from .html import Element
from .components import Component, MaterialIcon


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
