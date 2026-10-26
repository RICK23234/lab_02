# StreamStats

Потоковый анализатор событий в CSV и JSONL файлов. Читает файлы, считает статистику и записывает в JSON отчет

# Установка

``` bash
python -m venv venv 
source .\venv\bin\activate # Windows .\venv\Scripts\activate
pip install -e ".[dev]"
```

# Использование
``` bash
#Примеры

python -m streamstats analyze file.jsonl --format jsonl --output report.json
python -m streamstats analyze file1.jsonl file2.jsonl --format jsonl --output report.json --skip-invalid
python -m streamstats analyze file.csv --format csv --output report.json --top 3
```

При отсутвии --output отчет печается в консоль

# Структура
```
lab_02/
├── scr/
│    └── streamstats/
│        ├── __init__.py
│        ├── __main__.py
│        ├── analysis.py
│        ├── models.py
│        ├── parsers.py
│        ├── report.py
│        └── error.py
│
├── tests/
│    ├── data/
│    ├── analysis_test.py
│    ├── parsers_test.py
│    └── cli_test.py
├── pyproject.toml
└── README.md
```

# Тесты и линтер
``` bash
python -m pytest
ruff check .
```

