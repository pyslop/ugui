from ugui import App, Page

app = App(__name__)
app.ui.use("og")


@app.page("/", minify=False, style=True)
def index(page: Page):
    with page.body():
        with page.hero():
            page.hero.title("uGUI")
            page.hero.subtitle("Hello, World!")
            with page.hero.content():
                page.button("Click me", cls="primary", material_icon="cycle")


app.run()
