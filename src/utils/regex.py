import re

from datetime import datetime


def format_any_price(any_price_text: str) -> float | None:
    """Функция для очистки лишних данных и нормализации цены.

    Args:
        any_price_text (str): Текст с ценой.

    Returns:
        float: Очищенная и нормализованная цена.
    """

    if not any_price_text:
        return None

    pattern = r"[^\d,]"

    cleaned_price = re.sub(pattern, "", any_price_text)
    normalized_price = cleaned_price.replace(",", ".")

    try:
        return float(normalized_price)
    except ValueError:
        return None


def format_discount_info(discount_info_text: str) -> str | None:
    """Функция для очистки лишних данных от процента скидки.

    Args:
        discount_info_text (str): Текст с информацией о скидке.

    Returns:
        str: Процент скидки.
    """

    if not discount_info_text:
        return None

    pattern = r"[^\d\%]"

    cleaned_discount_info = re.sub(pattern, "", discount_info_text)

    return cleaned_discount_info


def format_offer_date(offer_date_text: str) -> str | None:
    """Функция для извлечения и форматирования даты и времени в формат ISO 8601.

    Args:
        offer_text (str): Текст с датой и временем окончания предложения.

    Returns:
        str: Форматированная дата и время в формате ISO 8601, или None, если не удалось извлечь.
    """

    if not offer_date_text:
        return None

    pattern = r"(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [APM]{2})"

    match = re.search(pattern, offer_date_text)

    if match:
        offer_date = match.group()
        formatted_offer_date = datetime.strptime(
            offer_date, "%m/%d/%Y %I:%M %p"
        )
        return formatted_offer_date.isoformat()

    return None
