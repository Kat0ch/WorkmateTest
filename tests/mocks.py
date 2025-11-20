# tests/mocks.py

from script import Employee, Begin


class DummyBegin:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.parser_args = type('', (), {})()
        self.parser_args.files = [str(self.file_path)]
        self.parser_args.report = ['employees']
        self.employees = []

    def _get_employees_from_files(self):
        return Begin._get_employees_from_files(self)
