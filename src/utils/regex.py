import re

from datetime import datetime


def format_any_price(any_price_text: str) -> float | None:
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
    if not discount_info_text:
        return None

    pattern = r"[^\d\%]"

    cleaned_discount_info = re.sub(pattern, "", discount_info_text)

    return cleaned_discount_info


def format_offer_date(offer_date_text: str) -> str | None:
    if not offer_date_text:
        return None

    pattern = r"(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [APM]{2})"

    match = re.search(pattern, offer_date_text)

    if match:
        offer_date = match.group()
        formatted_offer_date = datetime.strptime(
            offer_date, "%d/%m/%Y %I:%M %p"
        )
        return formatted_offer_date.isoformat()

    return None
