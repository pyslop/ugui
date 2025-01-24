from abc import ABC, abstractmethod
from typing import Any


class Component(ABC):
    def __init__(self, **props):
        self.props = props

    @abstractmethod
    def style(self) -> str:
        """Return the CSS for this component"""
        pass

    @abstractmethod
    def render(self, page: Any) -> Any:
        """Render the component using the page object"""
        pass

    def __call__(self, page: Any) -> Any:
        """Make components callable for convenience"""
        return self.render(page)


from .component import Component


class Card(Component):
    def style(self) -> str:
        return """
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

    def render(self, page):
        contents = self.props.get("contents", [])
        title = self.props.get("title")
        footer = self.props.get("footer")
        cls = f"card {self.props.get('class', '')}"

        with page.div(cls=cls.strip()) as card:
            if title:
                page.div(title, cls="card-header")
            with page.div(cls="card-body"):
                if isinstance(contents, (list, tuple)):
                    for content in contents:
                        page._current.append(content)
                else:
                    page._current.append(contents)
            if footer:
                page.div(footer, cls="card-footer")
        return card


class Form(Component):
    def style(self) -> str:
        return """
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

    def render(self, page):
        action = self.props.get("action", "#")
        method = self.props.get("method", "post")
        contents = self.props.get("contents", [])

        with page.form(action=action, method=method) as form:
            if isinstance(contents, (list, tuple)):
                for content in contents:
                    page._current.append(content)
            else:
                page._current.append(contents)
        return form


class Button(Component):
    def style(self) -> str:
        return """
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

    def render(self, page):
        text = self.props.get("text", "")
        cls = f"btn {self.props.get('class', '')}"
        props = {k: v for k, v in self.props.items() if k not in ["text", "class"]}
        return page.button(text, cls=cls.strip(), **props)


class Fieldset(Component):
    def style(self) -> str:
        return """
        fieldset {
            border: 1px solid #ddd;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        legend {
            padding: 0 0.5rem;
            font-weight: bold;
        }
        """

    def render(self, page):
        legend = self.props.get("legend")
        contents = self.props.get("contents", [])
        attrs = {k: v for k, v in self.props.items() if k not in ["legend", "contents"]}

        with page.fieldset(**attrs) as fs:
            if legend:
                page.legend(legend)
            for content in contents:
                page.append(content)
        return fs


class Field(Component):
    def style(self) -> str:
        return """
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
        """

    def render(self, page):
        label_text = self.props.get("label")
        input_type = self.props.get("input_type", "text")
        name = self.props.get("name")
        field_id = self.props.get("id", name or f"field_{input_type}_{id(label_text)}")

        attrs = {
            k: v
            for k, v in self.props.items()
            if k not in ["label", "input_type", "name", "id"]
        }

        with page.div(cls="form-field") as container:
            page.label(label_text, for_=field_id)
            page.input(type=input_type, id=field_id, name=name or field_id, **attrs)
        return container


# Keep BASE_CSS for page-wide styles
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
