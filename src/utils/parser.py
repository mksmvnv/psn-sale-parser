import requests

from bs4 import BeautifulSoup

from utils.regex import (
    format_any_price,
    format_discount_info,
    format_offer_date,
)
from config import settings


headers = {"User-Agent": settings.USER_AGENT}
proxies = {"http": settings.PROXY}


def get_total_pages(main_url: str) -> int:
    response = requests.get(main_url, headers=headers, proxies=proxies).content
    soup = BeautifulSoup(response, "html.parser")

    buttons = soup.find_all(
        "button",
        {"data-qa": lambda x: x and "#ems-sdk-top-paginator-root" in x},
    )

    max_page = 1

    for button in buttons:
        span = button.find("span", {"class": "psw-fill-x"})

        if span and span.text.strip().isdigit():
            max_page = max(max_page, int(span.text.strip()))

    return max_page


def get_category_urls(main_url: str) -> list:
    total_pages = get_total_pages(main_url)
    category_urls = [
        main_url + str(page) for page in range(1, total_pages + 1)
    ]

    return category_urls


def get_page_urls(category_url: str) -> list:
    response = requests.get(
        category_url, headers=headers, proxies=proxies
    ).content
    soup = BeautifulSoup(response, "html.parser")

    page_paths = soup.find_all("a", {"data-qa": True})
    page_urls = []

    for page_path in page_paths:
        if "EP" in page_path["href"]:
            page_urls.append(settings.DOMAIN_NAME + page_path["href"])

    return page_urls


def get_page_data(page_url: str) -> dict | None:
    response = requests.get(page_url, headers=headers, proxies=proxies).content
    soup = BeautifulSoup(response, "html.parser")

    name = soup.find("h1", {"data-qa": lambda x: x and "#name" in x})
    final_price = soup.find(
        "span", {"data-qa": lambda x: x and "#finalPrice" in x}
    )
    original_price = soup.find(
        "span", {"data-qa": lambda x: x and "#originalPrice" in x}
    )
    discount_info = soup.find(
        "span", {"data-qa": lambda x: x and "#discountInfo" in x}
    )
    offer_ends = soup.find(
        "span", {"data-qa": lambda x: x and "#discountDescriptor" in x}
    )

    page_data = {
        "name": name.text if name else None,
        "final_price": format_any_price(
            final_price.text if final_price else None
        ),
        "original_price": format_any_price(
            original_price.text if original_price else None
        ),
        "discount_info": format_discount_info(
            discount_info.text if discount_info else None
        ),
        "offer_ends": format_offer_date(
            offer_ends.text if offer_ends else None
        ),
    }

    if not page_data["final_price"]:
        return None

    return page_data
