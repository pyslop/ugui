from ugui import App, Page

app = App(__name__)


@app.page("/")
def index(page: Page):
    with page.head():
        page.title("µGUI Demo")
        page.meta(charset="utf-8")
        page.meta(name="viewport", content="width=device-width, initial-scale=1")

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
                    "Respects your mental context",
                    "Keeps code and ui in the same place",
                ),
                (
                    "Modern Stack",
                    "Built on ASGI/Quart for high performance",
                ),
                (
                    "Writing JavaScript is optional",
                    "No need to write or bundle JavaScript",
                ),
            ]:
                with page.div(cls="feature"):
                    page.h3(title)
                    page.p(desc)

        with page.div(cls="container"):
            page.ui.card(
                page.p("This is a sample card with a title and footer"),
                title="Sample Card",
                footer="Card Footer",
            )

            with page.ui.form(action="/login"):
                with page.ui.fieldset(legend="Login Details"):
                    page.ui.field("Username", name="username"),
                    page.ui.field("Password", input_type="password", name="password"),

                page.button("Submit", type="submit", cls="btn")


app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
