from typing import List

from line.message.template_messages import ERROR_MESSAGE, NO_MESSAGE
from splatoon.splatoon import Splatoon

RULE_NAMES = {
    "regular": "レギュラーマッチ",
    "bankara-challenge": "バンカラマッチ (チャレンジ)",
    "bankara-open": "バンカラマッチ (オープン)",
    "fest": "フェスマッチ",
    "x": "Xマッチ",
    "coop-grouping-regular": "サーモンラン",
}


# TODO: update format of text


def make_text(rule: str, stages: List[str]):
    text_head = f"【{RULE_NAMES[rule]}ステージ】"
    text_stages = "\n".join(f"・{stage}" for stage in stages)
    return f"{text_head}\n{text_stages}"


def get_message(rule: str, time: int = 0) -> str:
    if rule == "fest":
        return get_fes_message(time)
    elif rule == "coop-grouping-regular":
        return get_salmonrun_message(time)
    else:
        return get_battle_message(rule, time)


def get_battle_message(rule: str, time: int = 0) -> str:
    """
    message generator for regular, bankara, x
    """
    schedule = Splatoon.get_battle(rule, time)
    if not schedule:
        return ERROR_MESSAGE
    if schedule.festival:
        return NO_MESSAGE
    return make_text(rule, [st.name for st in schedule.stages])


def get_fes_message(time: int = 0) -> str:
    schedule = Splatoon.get_festival(time)
    if not schedule:
        return ERROR_MESSAGE
    if not schedule.festival:
        return NO_MESSAGE
    # before tricolor
    text = make_text(RULE_NAMES["fest"], [st.name for st in schedule.stages])
    if schedule.tricolor:
        text += f"【トリカラバトル】\n{schedule.tricolor_stage.name}"
    return text


def get_salmonrun_message(time: int = 0) -> int:
    schedule = Splatoon.get_salmonrun(time)
    if not schedule:
        return ERROR_MESSAGE
    weapons_str = "\n".join(f"・{w.name}" for w in schedule.weapons)
    text = f"【サーモンラン】\n{schedule.stage.name}\n{weapons_str}"
    return text
