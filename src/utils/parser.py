import requests

from bs4 import BeautifulSoup

from utils.regex import (
    format_any_price,
    format_discount_info,
    format_offer_date,
)

from config import settings

headers = {"User-Agent": settings.USER_AGENT}

proxies = {"http": settings.PROXIES}


def get_page_urls(category_url: str) -> list:
    """Функция для извлечения ссылок на страницы.

    Args:
        category_url (str): URL категории.

    Returns:
        list: Список ссылок на страницы.
    """

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
    """Функция для извлечения данных с каждой страницы.

    Args:
        page_url (str): URL страницы.

    Returns:
        dict: Словарь с данными.
    """

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
