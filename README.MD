# Скрипт для анализа сотрудников и формирования отчетов

## Запуск

Пример запуска с передачей файлов и типов отчетов:

```bash
python script.py --files employees1.csv employees2.csv --report employees performance
```

## Особенности

- Поддержка нескольких CSV-файлов для объединения данных.
- Возможность формирования нескольких отчетов
- Генерация отчетов в виде таблиц с помощью библиотеки tabulate.
- Возможность добавления новых типов отчетов

## Добавление новых отчетов

1. Создайте новый класс, наследующий EmployeesReport.
2. Определите нужные параметры и логику формирования отчета.
3. Добавьте его в словарь report_types в основном файле:

```python
report_types = {
    'employees': EmployeesReport,
    'performance': PerformanceEmployeesReport,
    'new_type': YourNewType,
}
```

4. Запустите скрипт с новым типом отчета:
```bash
python script.py --files employees1.csv --report new_type
```