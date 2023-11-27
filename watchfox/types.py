from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel

type CoordinateSystem = Literal['fox', 'ogs', 'kgs']
type Color = Literal['white', 'black']
type Winner = Literal['white', 'black', 'draw']
type Reason = Literal['resign', 'points']


@dataclass
class Result:
    winner: Winner
    reason: Reason | None = None
    points: float | None = None


class MinifoxPlayer(BaseModel):
    avatar: str
    country: str
    nick: str
    rank: str


class MinifoxSettings(BaseModel):
    board_size: int
    chinese_rules: bool
    handicap: int
    komi: int


class MinifoxTimeControl(BaseModel):
    byoyomi_periods: int
    byoyomi_time: int
    main_time: int


class MinifoxMatchStart(BaseModel):
    id: str
    black: MinifoxPlayer
    white: MinifoxPlayer
    settings: MinifoxSettings
    time_control: MinifoxTimeControl


class MinifoxMatchMove(BaseModel):
    id: str
    move: tuple[int, int]
    move_number: int
    turn: Literal['B', 'W']


class MinifoxTime(BaseModel):
    byoyomi: int
    byoyomi_time: int
    connected: bool
    disconnected_time: int
    main_time: int


class MinifoxMatchTime(BaseModel):
    id: str
    black_time: MinifoxTime
    white_time: MinifoxTime


class MinifoxMatchChat(BaseModel):
    id: str
    country: str
    nick: str
    rank: str
    message: str


class MinifoxMatchEnd(BaseModel):
    id: str
    result: str
