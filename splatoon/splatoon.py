from datetime import datetime
from typing import Any, Dict, Optional

import requests

from line.config import settings
from splatoon.scheme import Battle, Festival, SalmonRun, Stage, Weapon

MAX_REQUESTS = 3

TIME = {0: "now", 1: "next", 2: "schedule"}

HEADER = {"User-Agent": settings.USER_AGENT}


def str2datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+09:00")


def splatoon_api_url(rule, time: int = 0) -> str:
    return f"https://spla3.yuu26.com/api/{rule}/{TIME[time]}"


def get(url: str) -> Optional[Dict[str, Any]]:
    response = None
    for _ in range(MAX_REQUESTS):
        response = requests.get(url, headers=HEADER)
        if response.status_code == 200:
            break
    if response.status_code == 200:
        return response.json()
    else:
        return None


class Splatoon:
    def get_battle(rule: str, time: int = 0) -> Battle:
        response = get(splatoon_api_url(rule, time))
        if not response:
            return None
        response = response["results"][0]
        result = Battle(
            start=str2datetime(response["start_time"]),
            end=str2datetime(response["end_time"]),
            rule=None,
            stages=None,
            festival=response["is_fest"],
        )
        if not result.festival:
            result.rule = response["rule"]["name"]
            result.stages = [
                Stage(name=t["name"], img_url=t["image"]) for t in response["stages"]
            ]
        return result

    def get_festival(time: int = 0) -> Festival:
        response = get(splatoon_api_url("fest", time))
        if not response:
            return None
        response = response["results"][0]
        result = Festival(
            start=str2datetime(response["start_time"]),
            end=str2datetime(response["end_time"]),
            rule=None,
            stages=None,
            festival=response["is_fest"],
            tricolor=response["is_tricolor"],
            tricolor_stage=None,
        )
        if result.festival:
            result.rule = response["rule"]["name"]
            result.stages = [
                Stage(name=t["name"], img_url=t["image"]) for t in result["stagas"]
            ]
        if result.tricolor:
            result.tricolor_stage = Stage(
                name=result["tricolor_stage"]["name"],
                img_url=result["tricolor_stage"]["image"],
            )
        return result

    def get_salmonrun(time: int = 0) -> SalmonRun:
        response = get(splatoon_api_url("coop-grouping-regular", time))
        if not response:
            return None
        response = response["results"][0]
        result = SalmonRun(
            start=str2datetime(response["start_time"]),
            end=str2datetime(response["end_time"]),
            stage=Stage(
                name=response["stage"]["name"], img_url=response["stage"]["image"]
            ),
            weapons=[
                Weapon(name=w["name"], img_url=w["image"]) for w in response["weapons"]
            ],
        )
        return result
