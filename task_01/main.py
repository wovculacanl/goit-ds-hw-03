import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Create a .env file with a connection string..")

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1"),
    tlsCAFile=certifi.where(),
)

db = client.hw03
cats_collection = db.cats


# --- CREATE ---

def create_one(name: str, age: int, features: list[str]):
    """Creates a single cat entry in the collection."""
    try:
        result = cats_collection.insert_one(
            {
                "name": name,
                "age": age,
                "features": features,
            }
        )
        print(f"Кота '{name}' додано з _id: {result.inserted_id}")
        return result.inserted_id
    except PyMongoError as err:
        print(f"Помилка при додаванні кота: {err}")
        return None


def create_many(cats: list[dict]):
    """Creates multiple cat records in a single query."""
    if not cats:
        print("Порожній список — немає що додавати.")
        return None
    try:
        result = cats_collection.insert_many(cats)
        print(f"Успішно додано {len(result.inserted_ids)} котів.")
        return result.inserted_ids
    except PyMongoError as err:
        print(f"Помилка при масовому додаванні: {err}")
        return None


# --- READ ---

def get_all():
    """Gets all the cats in the collection."""
    try:
        cats = list(cats_collection.find())
        if not cats:
            print("Список порожній")
            return []
        for cat in cats:
            print(cat)
        return cats
    except PyMongoError as err:
        print(f"Помилка при отриманні списку котів: {err}")
        return None

def get_by_name(name: str):
    """Searches for a cat by name and returns a document."""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(f"Знайдено кота: {cat}")
            return cat
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
            return None
    except PyMongoError as err:
        print(f"Помилка при пошуку кота '{name}': {err}")
        return None


# --- UPDATE ---

def update_age_by_name(name: str, new_age: int):
    """Updates a cat's age, selected by name."""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено для оновлення.")
            return None
        print(f"Вік кота '{name}' успішно оновлено на {new_age}.")
        return result.modified_count
    except PyMongoError as err:
        print(f"Помилка при оновленні віку: {err}")
        return None


def add_features_by_name(name: str, new_features: str):
    """Adds a new characteristic to the cat's features list, selected by name."""
    try:
        result = cats_collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_features}},
        )
        if result.matched_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено.")
            return None
        if result.modified_count == 0:
            print(f"Характеристика '{new_features}' вже є у кота '{name}'.")
            return None
        else:
            print(f"Характеристику '{new_features}' додано коту '{name}'." )
            return result.modified_count
    except PyMongoError as err:
        print(f"Помилка при додаванні характеристики: {err}")
        return None


# --- DELETE ---

def delete_by_name(name: str):
    """Deletes a single cat, selected by name, from the collection."""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count == 0:
            print(f"Кота з ім'ям '{name}' не знайдено для видалення.")
            return None
        print(f"Кота '{name}' успішно видалено.")
        return result.deleted_count
    except PyMongoError as err:
        print(f"Помилка при видаленні кота: {err}")
        return None


def delete_all():
    """Deletes all entries from the collection."""
    try:
        result = cats_collection.delete_many({})
        print(f"Усі записи видалено. Кількість: {result.deleted_count}")
        return result.deleted_count
    except PyMongoError as err:
        print(f"Помилка при очищенні колекції: {err}")
        return None


# --- CLI ---

SAMPLE_CATS = [
    {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
    {"name": "murzik", "age": 5, "features": ["любить спати", "сірий"]},
    {"name": "simba", "age": 2, "features": ["грайливий", "полює на мух"]},
    {"name": "lord", "age": 7, "features": ["важний", "чорний", "муркотить"]},
]

MENU = """
=== Колекція котів ===
1 - показати всіх котів
2 - знайти кота за ім'ям
3 - оновити вік кота
4 - додати характеристику коту
5 - видалити кота за ім'ям
6 - видалити всіх котів
7 - додати одного кота
8 - наповнити колекцію прикладами
0 - вихід
"""


def _ask_age(prompt: str) -> int | None:
    """Читає вік з вводу; повертає int або None, якщо введено некоректно."""
    raw = input(prompt).strip()
    if not raw.isdigit():
        print("Вік має бути цілим невід'ємним числом.")
        return None
    return int(raw)


def run_cli():
    """Інтерактивне меню для роботи з колекцією."""
    while True:
        print(MENU)
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            print("Вихід.")
            break

        elif choice == "1":
            get_all()

        elif choice == "2":
            get_by_name(input("Ім'я кота: ").strip())

        elif choice == "3":
            name = input("Ім'я кота: ").strip()
            age = _ask_age("Новий вік: ")
            if age is not None:
                update_age_by_name(name, age)

        elif choice == "4":
            name = input("Ім'я кота: ").strip()
            feature = input("Нова характеристика: ").strip()
            add_features_by_name(name, feature)

        elif choice == "5":
            delete_by_name(input("Ім'я кота: ").strip())

        elif choice == "6":
            if input("Видалити ВСІ записи? (y/n): ").strip().lower() == "y":
                delete_all()
            else:
                print("Скасовано.")

        elif choice == "7":
            name = input("Ім'я кота: ").strip()
            age = _ask_age("Вік: ")
            if age is None:
                continue
            features = [
                f.strip()
                for f in input("Характеристики через кому: ").split(",")
                if f.strip()
            ]
            create_one(name, age, features)

        elif choice == "8":
            create_many(SAMPLE_CATS)

        else:
            print("Невідома команда.")


if __name__ == "__ma1in__":
    try:
        run_cli()
    except (KeyboardInterrupt, EOFError):
        print("\nВихід.")
