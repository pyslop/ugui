BASE_CSS = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body { 
    max-width: 800px; 
    margin: 0 auto;
    padding: 0.5rem;
    font-family: system-ui, sans-serif;
    line-height: 1.5;
    overflow-x: hidden;
}

nav { margin-bottom: 2rem; }
.hero { margin: 2rem 0; text-align: center; }
.features { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}
.feature { padding: 1rem; }
a { color: #0066cc; }
.container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 0.5rem;
}

@media (max-width: 640px) {
    .container { padding: 0.25rem; }
    body { padding: 0.25rem; }
}
"""

CARD_CSS = """
.card {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin: 1rem 0;
    overflow: hidden;
}
.card-header {
    padding: 1rem;
    border-bottom: 1px solid #ddd;
    background: #f8f9fa;
}
.card-body { padding: 1rem; }
.card-footer {
    padding: 1rem;
    border-top: 1px solid #ddd;
    background: #f8f9fa;
}
"""

FORM_CSS = """
.form-field {
    margin-bottom: 1rem;
    width: 100%;
    box-sizing: border-box;
}
.form-field label {
    display: block;
    margin-bottom: 0.5rem;
}
.form-field input {
    box-sizing: border-box;
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}
form { width: 100%; }
"""

BUTTON_CSS = """
.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: #0066cc;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    margin: 0.5rem;
}
.btn.secondary {
    background: transparent;
    border: 1px solid #0066cc;
    color: #0066cc;
}
"""
