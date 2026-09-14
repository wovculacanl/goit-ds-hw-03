# goit-ds-hw-03

Домашнє завдання: робота з MongoDB (Atlas) через PyMongo.

## Залежності

- Python `^3.14`
- `pymongo`
- `python-dotenv` — читання рядка підключення зі змінних середовища
- `certifi` — CA-сертифікати для TLS-підключення до MongoDB Atlas на macOS
- `requests`, `beautifulsoup4` — скрапінг (завдання 2)

## Встановлення

```bash
# встановити залежності у власне віртуальне середовище
poetry install

# створити .env з рядка-шаблону і вписати свій рядок підключення
cp .env.example .env
```

`.env` містить одну змінну `MONGO_URI` і не потрапляє в git (див. `.gitignore`).

## Завдання 1 — CRUD (`task_01/main.py`)

Кожен документ колекції `cats` має структуру:

```json
{
  "_id": "ObjectId(...)",
  "name": "barsik",
  "age": 3,
  "features": ["ходить в капці", "дає себе гладити", "рудий"]
}
```

### Реалізовані операції

| Операція | Функція |
| --- | --- |
| Створити один запис | `create_one(name, age, features)` |
| Створити кілька записів | `create_many(cats)` |
| Показати всі записи | `get_all()` |
| Знайти кота за ім'ям | `get_by_name(name)` |
| Оновити вік за ім'ям | `update_age_by_name(name, new_age)` |
| Додати характеристику за ім'ям | `add_features_by_name(name, new_features)` |
| Видалити запис за ім'ям | `delete_by_name(name)` |
| Видалити всі записи | `delete_all()` |

Усі функції обгорнуті в `try/except pymongo.errors.PyMongoError`.

### Запуск

```bash
poetry run python task_01/main.py
```

Скрипт показує інтерактивне меню; операції, що потребують даних (ім'я кота,
вік, характеристика), запитують їх через `input()`.

## Завдання 2 — скрапінг  (`task_02/`)

- `scrape.py` — парсить усі сторінки сайту, зберігає цитати в `qoutes.json` та авторів у `authors.json`
- `export_to_mongo.py` — читає ці файли й імпортує дані в колекції `qoutes` та `authors` хмарної бази Atlas

### Запуск

```bash
cd task_02
poetry run python scrape.py
poetry run python export_to_mongo.py
```
