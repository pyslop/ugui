from ugui import App, Page

app = App(__name__)


@app.page("/", minify=False)
def index(page: Page):
    with page.head():
        page.title("µGUI Demo")
        page.meta(charset="utf-8")
        page.meta(name="viewport", content="width=device-width, initial-scale=1")

    with page.body():
        # Navigation using new nav components
        with page.ui.navbar(direction="row"):
            page.ui.nav_item("Home", "/", icon="🏠")
            page.ui.nav_item("Docs", "/docs", icon="📚")

        # Hero section using new hero component
        with page.ui.hero() as hero:
            hero.title("µGUI Framework")
            hero.subtitle("A lightweight Python web framework for building UIs")
            with hero.content():
                page.ui.button("Get Started", href="#", cls="primary")
                page.ui.button("Learn More", href="#", cls="secondary")

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
            with page.ui.card() as card:

                with card.header():
                    page.h2("Login")

                with card.body():
                    with page.ui.form(action="/login"):
                        with page.ui.fieldset(legend="Login Details"):
                            page.ui.field("Username", name="username")
                            page.ui.field(
                                "Password", input_type="password", name="password"
                            )
                        page.ui.button("Submit", type="submit")

                with card.footer():
                    page.p("Don't have an account?")
                    page.a("Sign Up", href="/signup")


app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
