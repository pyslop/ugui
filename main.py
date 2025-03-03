from ugui import App, Page

app = App(__name__)


async def render_nav(page):
    with page.ui.navbar(direction="row"):
        page.ui.nav_item("Home", "/", material_icon="home", icon_color="auto")
        page.ui.nav_item(
            "Features", "/features", material_icon="star", icon_color="auto"
        )
        page.ui.nav_item(
            "Docs", "/docs", material_icon="description", icon_color="auto"
        )


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
                "scale",
                "hsl(200, 90%, 50%)",
                "Lightweight",
                "No bloat, linear payloads",
            ),
            (
                "bolt",
                "hsl(50, 90%, 50%)",
                "Modern",
                "Built on ASGI/Quart",
            ),
            (
                "psychology",
                "hsl(300, 90%, 50%)",
                "Contextual",
                "Colocate logic and interface",
            ),
            (
                "code_off",
                "hsl(100, 90%, 50%)",
                "Uncomplicated",
                "Built-in components",
            ),
        ]
        for icon, color, title, desc in features:
            with page.ui.box(material_icon=icon, icon_color=color):
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
                page.span("Don't have an account?")
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
        page.style(
            """
                .features { 
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 2rem;
                    margin: 2rem 0;
                }
                .feature { 
                    padding: 1rem; 
                    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
                }

                .container {
                    width: 100%;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 0.5rem;
                }
                """
        )

    with page.body():
        await render_nav(page)
        await render_hero(page)
        await render_features(page)
        await render_card(page)


app.run(host="0.0.0.0")
