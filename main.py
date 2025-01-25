from ugui import App, Page

app = App(__name__)


async def render_nav(page):
    with page.ui.navbar(direction="row"):
        page.ui.nav_item("Home", "/", material_icon="home")
        page.ui.nav_item("Docs", "/docs", material_icon="description")


async def render_hero(page):
    with page.ui.hero() as hero:
        hero.title("uGUI Framework")
        hero.subtitle("A lightweight Python web framework for building UIs")
        with hero.content():
            page.ui.button(
                "Get Started",
                href="#",
                cls="primary",
                material_icon="rocket_launch",
                title="Start building your first uGUI application",
            )
            page.ui.button(
                "Learn More",
                href="#",
                cls="secondary",
                material_icon="school",
                title="Read the documentation",
            )


async def render_features(page):
    with page.ui.grid(cols="auto-fit", min_width="350px", gap="2rem") as grid:
        features = [
            (
                "code",
                "Pragmatic",
                "Build web UIs with pure Python",
            ),
            (
                "rocket_launch",
                "Modern",
                "Built on ASGI/Quart for async I/O",
            ),
            (
                "psychology",
                "Contextual",
                "Keeps code and UI in the same place",
            ),
            (
                "gesture",
                "Uncomplicated",
                "No need to write or bundle JavaScript",
            ),
        ]

        for icon, title, desc in features:
            with page.ui.box(material_icon=icon):
                page.h3(title)
                page.p(desc)


async def render_card(page):
    with page.div(cls="container"):
        with page.ui.card() as card:

            with card.header(material_icon="account_circle"):
                page.h3("Login")

            with card.body():
                with page.ui.form(action="/login"):
                    with page.ui.fieldset(legend="Login Details"):
                        page.ui.field(
                            "Username",
                            name="username",
                            placeholder="Enter your username",
                            required=True,
                        )
                        page.ui.field(
                            "Password",
                            input_type="password",
                            name="password",
                            placeholder="Enter your password",
                            required=True,
                        )
                    page.ui.button(
                        "Submit",
                        type="submit",
                        material_icon="send",
                        title="Submit login form",
                    )

            with card.footer(material_icon="person_add"):
                page.p("Don't have an account?")
                page.ui.link(
                    "Sign Up",
                    "/signup",
                    material_icon="arrow_forward",
                    icon_position="right",
                    title="Create a new account",
                )


@app.page("/", minify=False, style=True)
async def index(page: Page):
    with page.head():
        page.title("uGUI Demo")

    with page.body():
        await render_nav(page)
        await render_hero(page)
        await render_features(page)
        await render_card(page)


app.run(host="0.0.0.0")
