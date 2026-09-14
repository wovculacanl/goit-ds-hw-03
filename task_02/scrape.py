import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


def parse_quotes():
    quotes = []
    author_urls = {}
    url = BASE_URL

    while url:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")

        for block in soup.find_all("div", class_="quote"):
            author = block.find("small", class_="author").text
            quotes.append({
                "tags": [tag.text for tag in block.find_all("a", class_="tag")],
                "author": author,
                "quote": block.find("span", class_="text").text,
            })

            if author not in author_urls:
                author_urls[author] = BASE_URL + block.find("a", href=lambda h: h and "/author/" in h)["href"]

        next_page = soup.find("li", class_="next")
        url = BASE_URL + next_page.find("a")["href"] if next_page else None

    return quotes, author_urls


def parse_authors(author_urls):
    authors = []
    for url in author_urls.values():
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        authors.append({
            "fullname": soup.find("h3", class_="author-title").text.strip(),
            "born_date": soup.find("span", class_="author-born-date").text.strip(),
            "born_location": soup.find("span", class_="author-born-location").text.strip(),
            "description": soup.find("div", class_="author-description").text.strip(),
        })
    return authors


if __name__ == "__main__":
    quotes_data, author_links = parse_quotes()
    authors_data = parse_authors(author_links)

    with open("qoutes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)

    print("Parsing results successfully saved to files")