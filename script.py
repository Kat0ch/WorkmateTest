import argparse
import csv
from tabulate import tabulate


class Employee:
    def __init__(self,
                 **kwargs
                 ) -> None:
        self.name: str = kwargs.get('name', '')
        self.position: str = kwargs.get('position', '')
        self.completed_tasks: int = int(kwargs.get('completed_tasks', 0))
        self.performance: float = float(kwargs.get('performance', 0.0))
        self.skills: list = kwargs.get('skills').split(', ')
        self.team: str = kwargs.get('team', '')
        self.experience_years: int = int(kwargs.get('experience_years', 0))


class Begin:
    def __init__(self):
        self._get_args()
        self._files: list[str] = self.parser_args.files
        self.reports: list[str] = self.parser_args.report
        self.employees: list[Employee] = self._get_employees_from_files()

    def _get_args(self) -> None:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument('--files', nargs='+', required=True)
        parser.add_argument('--report', nargs='+', required=True)
        self.parser_args: argparse.Namespace = parser.parse_args()

    def _get_employees_from_files(self) -> list[Employee]:
        employees = []
        for file in self.parser_args.files:
            try:
                with open(file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=',')
                    employees.extend([Employee(**row) for row in reader])
            except FileNotFoundError:
                print(f'Файл: {file} не найден')
        return employees


class EmployeesReport:
    _report: str = ''
    title: str = 'Отчет о сотрудниках'
    _rows_titles: list[str | None] = []
    sorted_by_column: int | None = None

    def __init__(self,
                 begin: Begin
                 ):
        self._employees: list[Employee] = begin.employees

    def _get_report_rows(self,
                         employee
                         ) -> list:
        if not self._rows_titles:
            self._rows_titles = list(vars(employee).keys())
        return [getattr(employee, title) for title in self._rows_titles]

    def generate_report(self) -> None:
        report_rows = [self._get_report_rows(employee) for employee in self._employees]
        if self.sorted_by_column is not None:
            report_rows.sort(key=lambda x: x[self.sorted_by_column], reverse=True)
        self._report = tabulate(report_rows, headers=self._rows_titles, tablefmt='grid')

    def get_report(self) -> None:
        print(self.title)
        print(self._report)


class PerformanceEmployeesReport(EmployeesReport):
    title: str = 'Отчет о производительности'
    _rows_titles: list[str] = ['name', 'position', 'performance']
    sorted_by_column: int | None = 2


if __name__ == '__main__':
    begin: Begin = Begin()

    report_types: dict[str: EmployeesReport] = {
        'employees': EmployeesReport,
        'performance': PerformanceEmployeesReport,
    }
    reports = []
    for report in begin.reports:
        try:
            reports.append(report_types[report](begin))
        except KeyError:
            print(f'Отчет с типом: {report} не найден')

    for report in reports:
        report.generate_report()
        report.get_report()
