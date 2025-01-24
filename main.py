from ugui import App, Page

app = App(__name__)


@app.page("/")
def index(page: Page):
    with page.head():
        page.title("µGUI Demo")
        page.meta(charset="utf-8")
        page.meta(name="viewport", content="width=device-width, initial-scale=1")

        # Minimal CSS
        with page.style():
            page.raw(
                """
                body { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 1rem;
                    font-family: system-ui, sans-serif;
                    line-height: 1.5;
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
            )

    with page.body():
        with page.nav():
            page.a("µGUI", href="/")

        with page.div(cls="hero"):
            page.h1("µGUI Framework")
            page.p("A lightweight Python web framework for building UIs")
            with page.div():
                page.a("Get Started", href="#", cls="btn")
                page.a("Learn More", href="#", cls="btn secondary")

        with page.div(cls="features"):
            for title, desc in [
                (
                    "Simple API",
                    "Build web UIs with pure Python using an intuitive API",
                ),
                (
                    "Respects developer's mental context",
                    "Keeps code and ui in the same place",
                ),
                (
                    "Modern Stack",
                    "Built on ASGI/Quart for high performance",
                ),
            ]:
                with page.div(cls="feature"):
                    page.h3(title)
                    page.p(desc)


app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
