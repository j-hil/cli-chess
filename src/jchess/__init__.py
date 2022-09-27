"""Init is required by some tooling."""

from datetime import date

def get_version():
    today = date.today()
    result = f"{today.year}.{today.month}.0"
    print(result)

__version__ = get_version()
