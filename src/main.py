import json

from utils.parser import (
    get_page_data,
    get_page_urls,
    get_category_urls,
)
from config import settings


main_url = settings.DOMAIN_NAME + settings.CATEGORY_PATH
json_path = settings.JSON_PATH


def main() -> None:
    sales = []
    page_urls = []
    category_urls = get_category_urls(main_url)

    for category_url in category_urls:
        page_urls.extend(get_page_urls(category_url))

    for page_url in page_urls:
        page_data = get_page_data(page_url)

        if page_data:
            sales.append(page_data)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4)


if __name__ == "__main__":
    main()
