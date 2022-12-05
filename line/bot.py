from datetime import datetime, timezone
from time import sleep
from typing import Dict, List

import schedule as task_scheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage

from config import settings
from line.message.messages import get_message, unify_messages
from splatoon.scheme import Festival
from splatoon.splatoon_schedule import splatoon_schedule

RULES = [
    "regular",
    "bankara-challenge",
    "bankara-open",
    "fest",
    "x",
    "coop-grouping-regular",
]


def updates_expected() -> bool:
    now = datetime.now(timezone.utc)
    return now.hour % 2 == 0


class LineBot:
    def __init__(self):
        self.line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
        self.festival: bool = None
        self.tricolor: bool = None
        self.start: Dict[str, datetime] = {rule: None for rule in RULES}

    def initialize(self) -> None:
        for rule in RULES:
            schedule = splatoon_schedule.get(rule)
            if schedule:
                self.start[rule] = schedule.start
                if rule == "fest":
                    self.festival = schedule.festival
                    self.tricolor = schedule.tricolor

    def get_update_messages(self, time: int = 0) -> List[str]:
        update_messages: List[str] = []
        if not updates_expected():
            return update_messages
        for rule in RULES:
            schedule = splatoon_schedule.get(rule, time)
            if schedule and self.start[rule] < schedule.start:
                if type(schedule) == Festival:
                    fes_start = not self.festival and schedule.festival
                    tricolor_start = not self.tricolor and schedule.tricolor
                    fes_end = self.festival and not schedule.festival
                    self.festival = schedule.festival
                    self.tricolor = schedule.tricolor
                    message = get_message(
                        schedule, rule, fes_start, tricolor_start, fes_end
                    )  # noqa
                else:
                    message = get_message(schedule, rule)
                if message:
                    update_messages.append(message.rstrip())
                self.start[rule] = schedule.start
        return update_messages

    def broadcast(self, text: str) -> None:
        messages = TextSendMessage(text=text)
        self.line_bot_api.broadcast(messages=messages)

    def send_updates(self):
        messages = self.get_update_messages()
        if messages:
            text = unify_messages(messages, init_message=True)
            self.broadcast(text=text)

    def run(self):
        self.initialize()
        task_scheduler.every().hour.at(":00").do(self.send_updates)
        while True:
            task_scheduler.run_pending()
            sleep(1)


line_bot = LineBot()

if __name__ == "__main__":
    line_bot.send_updates()
