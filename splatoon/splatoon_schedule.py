from datetime import datetime
from typing import Union

from splatoon.api import get_schedule
from splatoon.scheme import Battle, Festival, SalmonRun, Stage, Weapon


def str2datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+09:00")


class Splatoon:
    def get_battle(self, rule: str, time: int = 0) -> Battle:
        response = get_schedule(rule, time)
        if not response:
            return None
        response = response["results"][0]
        result = Battle(
            start=str2datetime(response["start_time"]),
            end=str2datetime(response["end_time"]),
            mode=None,
            stages=None,
            festival=response["is_fest"],
        )
        if not result.festival:
            result.mode = response["rule"]["name"]
            result.stages = [
                Stage(name=t["name"], img_url=t["image"]) for t in response["stages"]
            ]
        return result

    def get_festival(self, time: int = 0) -> Festival:
        response = get_schedule("fest", time)
        if not response:
            return None
        response = response["results"][0]
        result = Festival(
            start=str2datetime(response["start_time"]),
            end=str2datetime(response["end_time"]),
            mode=None,
            stages=None,
            festival=response["is_fest"],
            tricolor=response["is_tricolor"],
            tricolor_stage=None,
        )
        if result.festival:
            result.mode = response["rule"]["name"]
            result.stages = [
                Stage(name=t["name"], img_url=t["image"]) for t in result["stagas"]
            ]
        if result.tricolor:
            result.tricolor_stage = Stage(
                name=result["tricolor_stage"]["name"],
                img_url=result["tricolor_stage"]["image"],
            )
        return result

    def get_salmonrun(self, time: int = 0) -> SalmonRun:
        response = get_schedule("coop-grouping-regular", time)
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

    def get(self, rule: str, time: int = 0) -> Union[Battle, Festival, SalmonRun]:
        if rule == "fest":
            return self.get_festival(time)
        elif rule == "coop-grouping-regular":
            return self.get_salmonrun(time)
        else:
            return self.get_battle(rule, time)


splatoon_schedule = Splatoon()

if __name__ == "__main__":
    print(type(splatoon_schedule.get_battle("regular")))
    splatoon_schedule.get_festival()
    splatoon_schedule.get_salmonrun()
