from ugui import App, Page

app = App(__name__)


async def render_header(page):
    with page.header(cls="container"):
        with page.hgroup():
            page.h1("Pico")
            page.p("A pure HTML example, without dependencies.")

        with page.nav():
            with page.ul():
                with page.li():
                    with page.details(cls="dropdown"):
                        page.summary("Theme", role="button", cls="secondary")
                        with page.ul():
                            with page.li():
                                page.a("Auto", href="#", data_theme_switcher="auto")
                            with page.li():
                                page.a("Light", href="#", data_theme_switcher="light")
                            with page.li():
                                page.a("Dark", href="#", data_theme_switcher="dark")


async def render_preview_section(page):
    with page.section(id="preview"):
        page.h2("Preview")
        page.p(
            "Sed ultricies dolor non ante vulputate hendrerit. "
            "Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas."
        )

        with page.form():
            with page.div(cls="grid"):
                page.input(
                    type="text",
                    name="firstname",
                    placeholder="First name",
                    aria_label="First name",
                    required=True,
                )
                page.input(
                    type="email",
                    name="email",
                    placeholder="Email address",
                    aria_label="Email address",
                    autocomplete="email",
                    required=True,
                )
                page.button("Subscribe", type="submit")

            with page.fieldset():
                with page.label(for_="terms"):
                    page.input(type="checkbox", role="switch", id="terms", name="terms")
                    page.span(" I agree to the ")
                    page.a("Privacy Policy", href="#", onclick="event.preventDefault()")


async def render_typography_section(page):
    with page.section(id="typography"):
        page.h2("Typography")
        page.p(
            "Aliquam lobortis vitae nibh nec rhoncus. Morbi mattis neque eget efficitur feugiat. "
            "Vivamus porta nunc a erat mattis, mattis feugiat turpis pretium. Quisque sed tristique felis."
        )

        # Blockquote
        with page.blockquote():
            page.text(
                '"Maecenas vehicula metus tellus, vitae congue turpis hendrerit non. Nam at dui sit amet '
                'ipsum cursus ornare."'
            )
            with page.footer():
                page.cite("- Phasellus eget lacinia")

        # Lists section (moved inside typography)
        page.h3("Lists")
        with page.ul():
            page.li("Aliquam lobortis lacus eu libero ornare facilisis.")
            page.li("Nam et magna at libero scelerisque egestas.")
            page.li("Suspendisse id nisl ut leo finibus vehicula quis eu ex.")
            page.li("Proin ultricies turpis et volutpat vehicula.")

        # Inline text elements (moved inside typography)
        page.h3("Inline text elements")
        with page.div(cls="grid"):
            with page.p():
                page.a("Primary link", href="#", onclick="event.preventDefault()")
            with page.p():
                page.a(
                    "Secondary link",
                    href="#",
                    cls="secondary",
                    onclick="event.preventDefault()",
                )
            with page.p():
                page.a(
                    "Contrast link",
                    href="#",
                    cls="contrast",
                    onclick="event.preventDefault()",
                )

        with page.div(cls="grid"):
            with page.p():
                page.strong("Bold")
            with page.p():
                page.em("Italic")
            with page.p():
                page.u("Underline")

        with page.div(cls="grid"):
            with page.p():
                page._del("Deleted")
            with page.p():
                page.ins("Inserted")
            with page.p():
                page.s("Strikethrough")

        with page.div(cls="grid"):
            with page.p():
                page.small("Small")
            with page.p():
                with page.span("Text "):
                    page.sub("Sub")
            with page.p():
                with page.span("Text "):
                    page.sup("Sup")

        # Add missing inline elements
        with page.div(cls="grid"):
            with page.p():
                page.abbr("Abbr.", title="Abbreviation", data_tooltip="Abbreviation")
            with page.p():
                page.kbd("Kbd")
            with page.p():
                page.mark("Highlighted")

        # Headings section
        page.h3("Heading 3")
        page.p(
            "Integer bibendum malesuada libero vel eleifend. Fusce iaculis turpis ipsum, at efficitur "
            "sem scelerisque vel. Aliquam auctor diam ut purus cursus fringilla. Class aptent taciti "
            "sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."
        )

        page.h4("Heading 4")
        page.p(
            "Cras fermentum velit vitae auctor aliquet. Nunc non congue urna, at blandit nibh. "
            "Donec ac fermentum felis. Vivamus tincidunt arcu ut lacus hendrerit, eget mattis dui finibus."
        )

        page.h5("Heading 5")
        page.p(
            "Donec nec egestas nulla. Sed varius placerat felis eu suscipit. "
            "Mauris maximus ante in consequat luctus. Morbi euismod sagittis efficitur. "
            "Aenean non eros orci. Vivamus ut diam sem."
        )

        page.h6("Heading 6")
        page.p(
            "Ut sed quam non mauris placerat consequat vitae id risus. "
            "Vestibulum tincidunt nulla ut tortor posuere, vitae malesuada tortor molestie. "
            "Sed nec interdum dolor. Vestibulum id auctor nisi, a efficitur sem. "
            "Aliquam sollicitudin efficitur turpis, sollicitudin hendrerit ligula semper id. "
            "Nunc risus felis, egestas eu tristique eget, convallis in velit."
        )

        # Add Media section
        with page.figure():
            page.img(
                src="/static/img/aleksandar-jason-a562ZEFKW8I-unsplash.jpg",
                alt="Minimal landscape",
            )
            with page.figcaption():
                page.span("Image from ")
                page.a(
                    "unsplash.com",
                    href="https://unsplash.com/photos/a562ZEFKW8I",
                    target="_blank",
                )


async def render_buttons_section(page):
    with page.section(id="buttons"):
        page.h2("Buttons")
        with page.p(cls="grid"):
            page.button("Primary")
            page.button("Secondary", cls="secondary")
            page.button("Contrast", cls="contrast")

        with page.p(cls="grid"):
            page.button("Primary outline", cls="outline")
            page.button("Secondary outline", cls="outline secondary")
            page.button("Contrast outline", cls="outline contrast")


async def render_form_section(page):
    with page.section(id="form"):
        with page.form():
            page.h2("Form elements")

            # Search
            page.label("Search", for_="search")
            page.input(type="search", id="search", name="search", placeholder="Search")

            # Text
            page.label("Text", for_="text")
            page.input(type="text", id="text", name="text", placeholder="Text")
            page.small("Curabitur consequat lacus at lacus porta finibus.")

            # Select
            page.label("Select", for_="select")
            with page.select(id="select", name="select", required=True):
                page.option("Select…", value="", selected=True)
                page.option("…")

            # File browser
            with page.label("File browser", for_="file"):
                page.input(type="file", id="file", name="file")

            # Range slider
            with page.label("Range slider", for_="range"):
                page.input(
                    type="range",
                    min="0",
                    max="100",
                    value="50",
                    id="range",
                    name="range",
                )

            # States
            with page.div(cls="grid"):
                with page.label("Valid", for_="valid"):
                    page.input(
                        type="text",
                        id="valid",
                        name="valid",
                        placeholder="Valid",
                        aria_invalid="false",
                    )
                with page.label("Invalid", for_="invalid"):
                    page.input(
                        type="text",
                        id="invalid",
                        name="invalid",
                        placeholder="Invalid",
                        aria_invalid="true",
                    )
                with page.label("Disabled", for_="disabled"):
                    page.input(
                        type="text",
                        id="disabled",
                        name="disabled",
                        placeholder="Disabled",
                        disabled=True,
                    )

            # Date, Time, Color inputs
            with page.div(cls="grid"):
                with page.label("Date", for_="date"):
                    page.input(type="date", id="date", name="date")
                with page.label("Time", for_="time"):
                    page.input(type="time", id="time", name="time")
                with page.label("Color", for_="color"):
                    page.input(type="color", id="color", name="color", value="#0eaaaa")

            # Checkboxes, Radio buttons, Switches
            with page.div(cls="grid"):
                with page.fieldset():
                    with page.legend():
                        with page.strong():
                            page.text("Checkboxes")
                    with page.label("Checkbox", for_="checkbox-1"):
                        page.input(
                            type="checkbox",
                            id="checkbox-1",
                            name="checkbox-1",
                            checked=True,
                        )
                    with page.label("Checkbox", for_="checkbox-2"):
                        page.input(type="checkbox", id="checkbox-2", name="checkbox-2")

                with page.fieldset():
                    with page.legend():
                        with page.strong():
                            page.text("Radio buttons")
                    with page.label("Radio button", for_="radio-1"):
                        page.input(
                            type="radio",
                            id="radio-1",
                            name="radio",
                            value="radio-1",
                            checked=True,
                        )
                    with page.label("Radio button", for_="radio-2"):
                        page.input(
                            type="radio", id="radio-2", name="radio", value="radio-2"
                        )

                with page.fieldset():
                    with page.legend():
                        with page.strong():
                            page.text("Switches")
                    with page.label("Switch", for_="switch-1"):
                        page.input(
                            type="checkbox",
                            id="switch-1",
                            name="switch-1",
                            role="switch",
                            checked=True,
                        )
                    with page.label("Switch", for_="switch-2"):
                        page.input(
                            type="checkbox",
                            id="switch-2",
                            name="switch-2",
                            role="switch",
                        )

            # Add form buttons at the bottom
            page.input(type="reset", value="Reset", onclick="event.preventDefault()")
            page.input(type="submit", value="Submit", onclick="event.preventDefault()")


async def render_tables_section(page):
    with page.section(id="tables"):
        page.h2("Tables")
        with page.div(cls="overflow-auto"):
            with page.table(cls="striped"):
                with page.thead():
                    with page.tr():
                        for text in [
                            "#",
                            "Heading",
                            "Heading",
                            "Heading",
                            "Heading",
                            "Heading",
                            "Heading",
                            "Heading",
                        ]:
                            page.th(text, scope="col")
                with page.tbody():
                    for i in range(1, 4):
                        with page.tr():
                            page.th(str(i), scope="row")
                            for _ in range(7):
                                page.td("Cell")


async def render_modal_section(page):
    with page.section(id="modal"):
        page.h2("Modal")
        page.button(
            "Launch demo modal",
            cls="contrast",
            data_target="modal-example",
            onclick="toggleModal(event)",
        )

    # Modal dialog
    with page.dialog(id="modal-example"):
        with page.article():
            with page.header():
                page.button(
                    aria_label="Close",
                    rel="prev",
                    data_target="modal-example",
                    onclick="toggleModal(event)",
                )
                page.h3("Confirm your action!")
            page.p(
                "Cras sit amet maximus risus. Pellentesque sodales odio sit amet augue finibus pellentesque."
            )
            with page.footer():
                page.button(
                    "Cancel",
                    role="button",
                    cls="secondary",
                    data_target="modal-example",
                    onclick="toggleModal(event)",
                )
                page.button(
                    "Confirm",
                    autofocus=True,
                    data_target="modal-example",
                    onclick="toggleModal(event)",
                )


async def render_additional_sections(page):
    # Accordions
    with page.section(id="accordions"):
        page.h2("Accordions")
        with page.details():
            page.summary("Accordion 1")
            page.p("Lorem ipsum dolor sit amet, consectetur adipiscing elit...")
        with page.details(open=True):
            page.summary("Accordion 2")
            with page.ul():
                page.li("Vestibulum id elit quis massa interdum sodales.")
                page.li("Nunc quis eros vel odio pretium tincidunt nec quis neque.")
                page.li("Quisque sed eros non eros ornare elementum.")
                page.li("Cras sed libero aliquet, porta dolor quis, dapibus ipsum.")

    # Article
    with page.article(id="article"):
        page.h2("Article")
        page.p(
            "Nullam dui arcu, malesuada et sodales eu, efficitur vitae dolor. "
            "Sed ultricies dolor non ante vulputate hendrerit. "
            "Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas. "
            "Nunc placerat facilisis cursus. Sed vestibulum metus eget dolor pharetra rutrum."
        )
        with page.footer():
            page.small("Duis nec elit placerat, suscipit nibh quis, finibus neque.")

    # Group
    with page.section(id="group"):
        page.h2("Group")
        with page.form():
            with page.fieldset(role="group"):
                page.input(
                    name="email",
                    type="email",
                    placeholder="Enter your email",
                    autocomplete="email",
                )
                page.input(type="submit", value="Subscribe")

    # Progress
    with page.section(id="progress"):
        page.h2("Progress bar")
        page.progress(id="progress-1", value="25", max="100")
        page.progress(id="progress-2")

    # Loading
    with page.section(id="loading"):
        page.h2("Loading")
        # Create a truly empty article with only aria-busy attribute
        with page.article(aria_busy="true"):
            pass
        page.button("Please wait…", aria_busy="true")


@app.page(
    "/",
    minify=False,
    style="/static/css/pico/pico.min.css",
)
async def index(page: Page):
    with page.head():
        page.title("Preview • Pico CSS")
        page.meta(charset="utf-8")
        page.meta(name="viewport", content="width=device-width, initial-scale=1")
        page.meta(name="color-scheme", content="light dark")
        page.meta(
            name="description", content="A pure HTML example, without dependencies."
        )
        # Add script tags
        # page.script(src="js/minimal-theme-switcher.js")
        # page.script(src="js/modal.js")

    with page.body():
        await render_header(page)

        with page.main(cls="container"):
            await render_preview_section(page)
            await render_typography_section(page)
            await render_buttons_section(page)
            await render_form_section(page)
            await render_tables_section(page)
            await render_modal_section(page)
            await render_additional_sections(page)

        with page.footer(cls="container"):
            with page.small():
                page.span("Built with ")
                page.a("Pico", href="https://picocss.com")
                page.span(" • ")
                page.a(
                    "Source code",
                    href="https://github.com/picocss/examples/blob/master/v2-html/index.html",
                )


app.run()
