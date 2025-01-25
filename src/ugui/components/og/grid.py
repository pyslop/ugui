from . import Component


class Grid(Component):
    def __init__(self, **props):
        cols = props.pop("cols", "auto-fit")
        min_width = props.pop("min_width", "250px")
        gap = props.pop("gap", "1rem")
        props["class"] = "grid"

        super().__init__("div", **props)
        self.cols = cols
        self.min_width = min_width
        self.gap = gap

    def style(self) -> str:
        return f"""
        .grid {{
            display: grid;
            grid-template-columns: repeat({self.cols}, minmax({self.min_width}, 1fr));
            gap: {self.gap};
            width: 100%;
            margin: 1rem 0;
        }}
        """
