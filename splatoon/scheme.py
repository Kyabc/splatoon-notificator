from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Stage(BaseModel):
    name: str
    img_url: str


class Weapon(BaseModel):
    name: str
    img_url: str


class Battle(BaseModel):
    start: datetime
    end: datetime
    rule: Optional[str]
    stages: Optional[List[Stage]]
    festival: bool


class Festival(BaseModel):
    start: datetime
    end: datetime
    rule: Optional[str]
    stages: Optional[List[Stage]]
    festival: bool
    tricolor: bool
    tricolor_stage: Optional[Stage]


class SalmonRun(BaseModel):
    start: datetime
    end: datetime
    stage: Stage
    weapons: List[Weapon]
