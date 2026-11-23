"""Reusable defensive validation helpers."""
import re
from typing import Optional

CITY_RE = re.compile(r"^[\w .,'-]{1,80}$", re.UNICODE)

class ValidationError(ValueError):
    """Raised when user-supplied data fails validation."""

def validate_city(city: str) -> str:
    city = (city or "").strip()
    if not city:
        raise ValidationError("City cannot be blank.")
    if len(city) > 80 or not CITY_RE.fullmatch(city):
        raise ValidationError("Enter a valid city name (1–80 characters).")
    return city

def validate_float(value, field: str, minimum: Optional[float] = None, maximum: Optional[float] = None) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a number.")
    if number != number or number in (float("inf"), float("-inf")):
        raise ValidationError(f"{field} must be finite.")
    if minimum is not None and number < minimum:
        raise ValidationError(f"{field} must be at least {minimum}.")
    if maximum is not None and number > maximum:
        raise ValidationError(f"{field} must be at most {maximum}.")
    return number

def validate_coordinates(latitude, longitude):
    return (validate_float(latitude, "Latitude", -90, 90), validate_float(longitude, "Longitude", -180, 180))
