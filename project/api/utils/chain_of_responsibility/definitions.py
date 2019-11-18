from __future__ import annotations
from abc import ABC, abstractmethod


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    def handle(self, request, row):
        pass


class AbstractHandler(Handler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def handle(self, request, row):
        if self._next_handler:
            return self._next_handler.handle(request, row)

        return None
