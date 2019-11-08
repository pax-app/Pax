from project.api.utils.chain_of_responsibility.handlers import CreateHandler, UpdateHandler, UpdateStateHandler, ErrorHandler


class UpCreate():
    _create = CreateHandler()
    _update = UpdateHandler()
    _error = ErrorHandler()

    def __init__(self):
        self._create.set_next(self._update).set_next(self._error)

    def execute(self, request, row):
        return self._create.handle(request, row)


class UpdateState():
    _update = UpdateStateHandler()
    _error = ErrorHandler()

    def __init__(self):
        self._update.set_next(self._error)

    def execute(self, request, row):
        return self._update.handle(request, row)
