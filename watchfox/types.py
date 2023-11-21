from dataclasses import dataclass
from typing import Literal, TypedDict

type Color = Literal['white', 'black']
type Winner = Literal['white', 'black', 'draw']
type Reason = Literal['resign', 'points']


@dataclass
class Result:
    winner: Winner
    reason: Reason | None = None
    points: float | None = None


class MinifoxPlayer(TypedDict):
    avatar: str
    country: str
    nick: str
    rank: str


class MinifoxSettings(TypedDict):
    board_size: int
    chinese_rules: bool
    handicap: int
    komi: int


class MinifoxTimeControl(TypedDict):
    byoyomi_periods: int
    byoyomi_time: int
    main_time: int


class MinifoxMatchStart(TypedDict):
    id: str
    black: MinifoxPlayer
    white: MinifoxPlayer
    settings: MinifoxSettings
    time_control: MinifoxTimeControl


class MinifoxMatchMove(TypedDict):
    id: str
    move: tuple[int, int]
    move_number: int
    turn: Literal['B', 'W']


class MinifoxTime(TypedDict):
    byoyomi: int
    byoyomi_time: int
    connected: bool
    disconnected_time: int
    main_time: int


class MinifoxMatchTime(TypedDict):
    id: str
    black_time: MinifoxTime
    white_time: MinifoxTime


class MinifoxMatchChat(TypedDict):
    id: str
    country: str
    nick: str
    rank: str
    message: str


class MinifoxMatchEnd(TypedDict):
    id: str
    result: str
