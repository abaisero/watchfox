import asyncio
import logging
import os
import re
import time
from typing import AsyncIterator, Final, Iterator

from watchfox import PACKAGE_DIR
from watchfox.types import Color, CoordinateSystem, MinifoxMatchStart, Result

logger = logging.getLogger(__name__)


def sleep_iterator[T](it: Iterator[T], sleep: float) -> Iterator[T]:
    for item in it:
        time.sleep(sleep)
        yield item


async def async_sleep_iterator[T](it: Iterator[T], sleep: float) -> AsyncIterator[T]:
    for item in it:
        await asyncio.sleep(sleep)
        yield item


B_or_W_to_winner: Final[dict[str, Color]] = {'B': 'black', 'W': 'white'}


def parse_result(result: str) -> Result:
    if re.match(r'^Draw$', result):
        return Result('draw')

    if match := re.match(r'^(?:((B|W))\+ )?(Draw|Resign)$', result):
        B_or_W = match.group(1)

        winner = B_or_W_to_winner[B_or_W]
        return Result(winner, 'resign')

    # many cases still missing for now
    # TODO: eventually this should become a ValueError
    raise NotImplementedError(f'invalid {result=}')


def get_nick_color(data: MinifoxMatchStart, nick: str) -> Color:
    logger.info(f'searching color for {nick=}')

    if data.black.nick == nick:
        logger.info(f'color for {nick=} found black')
        return 'black'

    if data.white.nick == nick:
        logger.info(f'color for {nick=} found white')
        return 'white'

    raise ValueError(f'{nick=} not found')


def make_assets_filename(filename: str) -> str:
    return os.path.join(PACKAGE_DIR, 'assets', filename)


def make_move_audio_filename(
    system: CoordinateSystem,
    color: Color,
    move: tuple[int, int],
):
    i, j = move
    return make_assets_filename(f'audio/{system}/{color}.{i}.{j}.mp3')
