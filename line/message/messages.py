from typing import Union

from line.message.template_messages import (
    ERROR_MESSAGE,
    FESTIVAL_END,
    FESTIVAL_START,
    NO_MESSAGE,
    TRICOLOR_START,
    header,
    mode_message,
    stages_message,
    time_message,
    weapons_message,
)
from splatoon.scheme import Battle, Festival, SalmonRun


def get_message(
    schedule: Union[Battle, Festival, SalmonRun],
    rule: str,
    fes_start: bool = False,
    tricolor_start: bool = False,
    fes_end: bool = False,
) -> str:
    if type(schedule) == Battle:
        return get_battle_message(schedule, rule)
    elif type(schedule) == Festival:
        return get_fes_message(
            schedule, rule, fes_start, tricolor_start, fes_end
        )  # noqa
    else:
        return get_salmonrun_message(schedule, rule)


def get_battle_message(schedule: Battle, rule: str) -> str:
    if not schedule:
        return ERROR_MESSAGE
    if schedule.festival:
        return NO_MESSAGE
    text = (
        header(rule)
        + time_message(schedule.start, schedule.end)
        + mode_message(schedule.mode)
        + stages_message(schedule.stages)
    )
    return text


def get_fes_message(
    schedule: Festival, rule: str, fes_start: bool, tricolor_start: bool, fes_end: bool
) -> str:
    if not schedule:
        return ERROR_MESSAGE
    if not schedule.festival:
        return NO_MESSAGE
    # before tricolor
    text = (
        header(rule)
        + time_message(schedule.start, schedule.end)
        + mode_message(schedule.mode)
        + stages_message(schedule.stages)
    )
    if schedule.tricolor:
        text += header("tricolor") + stages_message([schedule.tricolor_stage])
        if tricolor_start:
            text = TRICOLOR_START + text
    if fes_start:
        text = FESTIVAL_START + text
    if fes_end:
        text = FESTIVAL_END + text
    return text


def get_salmonrun_message(schedule: SalmonRun, rule: str) -> int:
    # TODO: クマさん武器に対応
    if not schedule:
        return ERROR_MESSAGE
    text = (
        header(rule)
        + time_message(schedule.start, schedule.end)
        + stages_message([schedule.stage])
        + weapons_message(schedule.weapons)
    )
    return text
