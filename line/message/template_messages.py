from datetime import datetime
from typing import List, Union

from splatoon.scheme import Stage, Weapon

RULE_NAMES = {
    "regular": "レギュラーマッチ",
    "bankara-challenge": "バンカラマッチ（チャレンジ）",
    "bankara-open": "バンカラマッチ（オープン）",
    "fest": "フェスマッチ",
    "tricolor": "トリカラバトル",
    "x": "Xマッチ",
    "coop-grouping-regular": "サーモンラン",
}

ERROR_MESSAGE = "エラーによりスケジュールが取得できませんでした"
NO_MESSAGE = ""
FESTIVAL_START = "🏮イカフェスが開始しました！"
TRICOLOR_START = "💈トリカラバトルが開始しました！"
FESTIVAL_END = "🏮イカフェスが終了しました！"
INIT_MESSAGE = "スケジュールが更新されました！🦑"


def datetime2str(dt: datetime) -> str:
    return dt.strftime("%-m/%-d %H:%M")


def oneline(ls: List[Union[Stage, Weapon]], sep: str = "、") -> str:
    return sep.join(s.name for s in ls)


def header(rule: str) -> str:
    if rule not in RULE_NAMES:
        return "ERROR"
    return f"【{RULE_NAMES[rule]}】\n"


def time_message(start: datetime, end: datetime) -> str:
    return f"⏰ {datetime2str(start)} - {datetime2str(end)}\n"


def stages_message(stages: List[Stage]) -> str:
    return f"🏞 {oneline(stages)}\n"


def weapons_message(weapons: List[Weapon]) -> str:
    return f"🔫 {oneline(weapons)}\n"


def mode_message(mode: str) -> str:
    return f"📌 {mode}\n"
