import sys
import unittest

import pytest
import script
from script import Employee, EmployeesReport, PerformanceEmployeesReport, Begin
from tests.mocks import DummyBegin


@pytest.fixture
def sample_employees_csv():
    return """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
Sarah Johnson,Fullstack Developer,47,4.7,"JavaScript, Node.js, React, MongoDB",Web Team,5
"""


class TestEmployee:
    def test_employee_init(self):
        data = {
            'name': 'Ivan Ivanov',
            'position': 'Developer',
            'completed_tasks': '10',
            'performance': '75.5',
            'skills': 'Python, SQL',
            'team': 'Backend',
            'experience_years': '3'
        }
        emp = Employee(**data)
        assert emp.name == 'Ivan Ivanov'
        assert emp.completed_tasks == 10
        assert emp.skills == ['Python', 'SQL']
        assert emp.experience_years == 3


class TestBegin:
    def test_get_args(self, monkeypatch):
        monkeypatch.setattr('sys.argv', ['script.py', '--files', 'file1', 'file2', '--report', 'rep1'])
        begin = Begin()
        assert begin._files == ['file1', 'file2']
        assert 'rep1' in begin.reports

    def test_get_employees_from_files(self, tmp_path, sample_employees_csv):
        file_path = tmp_path / "employees.csv"
        file_path.write_text(sample_employees_csv, encoding='utf-8')
        begin = DummyBegin(file_path)
        employees = begin._get_employees_from_files()
        assert len(employees) == 6
        assert employees[0].name == 'Alex Ivanov'


class TestEmployeesReport:
    def test_generate_report(self):
        emp1 = Employee(name='Ivan', position='Dev', completed_tasks=10, performance=80.0, skills='Python',
                        team='Backend', experience_years=2)
        emp2 = Employee(name='Maria', position='Manager', completed_tasks=5, performance=90.0, skills='Management',
                        team='HR', experience_years=4)
        report = EmployeesReport(DummyBegin())
        report._employees = [emp1, emp2]
        report.generate_report()
        report.get_report()
        assert 'Ivan' in report._report
        assert 'Maria' in report._report


class TestPerformanceEmployeesReport:
    def test_sorting(self):
        emp1 = Employee(name='Ivan', position='Dev', completed_tasks=10, performance=80.0, skills='Python',
                        team='Backend', experience_years=2)
        emp2 = Employee(name='Maria', position='Manager', completed_tasks=5, performance=90.0, skills='Management',
                        team='HR', experience_years=4)
        report = PerformanceEmployeesReport(DummyBegin())
        report._employees = [emp1, emp2]
        report.generate_report()
        first_line = report._report.splitlines()[3]
        assert 'Maria' in first_line
