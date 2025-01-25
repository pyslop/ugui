from ugui import App, Page

app = App(__name__)


@app.page("/", minify=False, style=False)
def index(page: Page):
    with page.body():
        page.h1("Hello, World!")


app.run()
