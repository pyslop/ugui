from ugui import App, Page

app = App(__name__)
app.use("plain")


@app.page("/", minify=False, style=True)
def index(page: Page):
    with page.body():
        # with page.hero():
        #     page.hero.title("uGUI")
        #     page.hero.subtitle("Hello, World!")
        #     with page.hero.content():
        #         page.button("Click me", cls="primary", material_icon="cycle")
        with page.box(material_icon="cycle"):
            page.h1("Hello, World!")
            page.p("This is a simple example of uGUI.")

        with page.main():
            page.h3("Here's some main content")
            page.p("Because that what we have on the menu today.")


app.run()
