from typing import Any, Dict, Optional

import requests

from config import settings

HEADER = {"User-Agent": settings.USER_AGENT}

TIME = {0: "now", 1: "next", 2: "schedule"}


def endpoint(rule: str, time: int = 0) -> str:
    return f"https://spla3.yuu26.com/api/{rule}/{TIME[time]}"


def get_schedule(rule: str, time: int = 0) -> Optional[Dict[str, Any]]:
    url = endpoint(rule, time)
    response = None
    for _ in range(settings.MAX_API_REQUESTS):
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:
            break
    if response.status_code == 200:
        return response.json()
    else:
        return None


if __name__ == "__main__":
    schedule = get_schedule("regular")
    print(schedule)
