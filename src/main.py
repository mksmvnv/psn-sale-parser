import json

from utils.parser import (
    get_page_data,
    get_page_urls,
)

from config import settings


def main() -> None:
    """Основная функция."""

    all_pages_data = []
    page_urls = get_page_urls(settings.CATEGORY_URL)

    for page_url in page_urls:
        page_data = get_page_data(page_url)

        if page_data:
            all_pages_data.append(page_data)

    with open("./src/json/all_pages_data.json", "w", encoding="utf-8") as f:
        json.dump(all_pages_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
