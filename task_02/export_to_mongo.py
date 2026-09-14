import json
import os
import certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Create a .env file with a connection string.")


def main():
    client = MongoClient(
        MONGO_URI,
        server_api=ServerApi("1"),
        tlsCAFile=certifi.where(),
    )
    db = client.quotes

    try:
        with open("qoutes.json", encoding="utf-8") as f:
            quotes = json.load(f)

        with open("authors.json", encoding="utf-8") as f:
            authors = json.load(f)

        if quotes:
            db.qoutes.delete_many({})  # Очищення перед імпортом
            db.qoutes.insert_many(quotes)
            print(f"Imported {len(quotes)} quotes into the 'qoutes' collection")

        if authors:
            db.authors.delete_many({})
            db.authors.insert_many(authors)
            print(f"Imported {len(authors)} authors into the 'authors' collection")

        print("Records successfully added to the database!")

    except FileNotFoundError as err:
        print(f"Помилка: не знайдено файл — {err.filename}")
    except PyMongoError as err:
        print(f"Помилка при роботі з MongoDB: {err}")
    finally:
        client.close()


if __name__ == "__main__":
    main()