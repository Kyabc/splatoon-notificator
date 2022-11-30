from linebot import LineBotApi
from linebot.models import TextSendMessage

from line.config import settings
from line.message.messages import get_message
import schedule

RULES = [
    "regular",
    "bankara-challenge",
    "bankara-open",
    "fest",
    "x",
    "coop-grouping-regular",
]


class LineBot:
    def __init__(self):
        self.line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
        self.festival = None
        self.tricolor = None

    def send(self):
        text = "\n".join(get_message(rule, 0) for rule in RULES)
        messages = TextSendMessage(text=text)
        self.line_bot_api.broadcast(messages=messages)

    def run(self):
        schedule.every().hour.at(":00").do(self.send())

line_bot = LineBot()

if __name__ == "__main__":
    line_bot.run()
