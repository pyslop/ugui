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
    font-size: var(--font-size);
    font-family: var(--font-family);
    color: var(--color-text);
    background: var(--color-bg);
    transition: background 0.2s ease, color 0.2s ease;
}
"""
