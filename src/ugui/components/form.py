from . import Component, Element


class Form(Component):
    def __init__(self, **props):
        # Extract form-specific props
        action = props.pop("action", "#")
        method = props.pop("method", "post")

        # Initialize with form attributes
        super().__init__("form", action=action, method=method, **props)

        # Handle contents after initialization
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                self.append(content)
        else:
            self.append(contents)

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


class Fieldset(Component):
    def __init__(self, **props):
        # Extract fieldset-specific props
        legend = props.pop("legend", None)

        # Initialize with remaining props
        super().__init__("fieldset", **props)

        # Add legend if provided
        if legend:
            legend_elem = Element("legend")
            legend_elem.append(legend)
            self.append(legend_elem)

        # Handle contents after initialization
        contents = props.get("contents", [])
        if isinstance(contents, (list, tuple)):
            for content in contents:
                self.append(content)
        else:
            self.append(contents)

    def style(self) -> str:
        return """
        fieldset {
            border: 0.0625rem solid var(--color-border);
            padding: 1rem;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
            background: var(--color-bg);
        }
        legend {
            padding: 0 0.5rem;
            font-weight: bold;
            color: var(--color-text);
            background: var(--color-bg);
        }
        """


class Field(Component):
    def __init__(self, **props):
        super().__init__("div", cls="form-field", **props)
        label_text = self.props.get("label")
        input_type = self.props.get("input_type", "text")
        name = self.props.get("name")
        field_id = self.props.get("id", name or f"field_{input_type}_{id(label_text)}")

        attrs = {
            k: v
            for k, v in self.props.items()
            if k not in ["label", "input_type", "name", "id"]
        }

        # Create and append label element
        label = Element("label", for_=field_id)
        label.append(label_text)
        self.append(label)

        # Create and append input element
        self.append(
            Element(
                "input", type=input_type, id=field_id, name=name or field_id, **attrs
            )
        )

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
            color: var(--color-text);
        }
        .form-field input {
            box-sizing: border-box;
            width: 100%;
            padding: 0.5rem;
            border: 0.0625rem solid var(--color-border);
            border-radius: 0.25rem;
            background: var(--color-bg);
            color: var(--color-text);
        }
        .form-field input:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 2px var(--color-primary-bg);
        }
        .form-field input::placeholder {
            color: var(--color-text-secondary);
        }
        """
