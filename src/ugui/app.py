from pathlib import Path
from asgiref.sync import sync_to_async
from quart import Quart, request, send_from_directory
from .page import Page
import inspect


class App(Quart):
    def __init__(self, *args, **kwargs):
        # Set static folder before initializing Quart
        if "static_folder" not in kwargs:
            kwargs["static_folder"] = str(Path(__file__).parent / "static")

        super().__init__(*args, **kwargs)
        self._pages = []

        # Override static url path if needed
        if "static_url_path" not in kwargs:
            self.static_url_path = "/static"

    async def handle_page(self, func, minify=True, style=True):
        page = Page(minify=minify, style=style)
        if inspect.iscoroutinefunction(func):
            await func(page)
        else:
            await sync_to_async(func)(page)
        return str(page)

    def page(self, route, minify=True, style=True):
        def decorator(func):
            async def wrapper():
                return await self.handle_page(func, minify=minify, style=style)

            self._pages.append((route, wrapper))
            return wrapper

        return decorator

    def run(self, host="127.0.0.1", port=5000, debug=True, use_reloader=True):
        for route, func in self._pages:
            self.route(route)(func)

        super().run(host=host, port=port, debug=debug, use_reloader=use_reloader)
