import logging
import re
import time
from typing import Iterator, cast, Final

from watchfox.types import Color, MinifoxMatchStart, Result

logger = logging.getLogger(__name__)


def sleep_iterator[T](it: Iterator[T], sleep: float) -> Iterator[T]:
    for item in it:
        time.sleep(sleep)
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
    for color in ['white', 'black']:
        if data[color]['nick'] == nick:
            logger.info(f'color for {nick=} found {color=}')
            return cast(Color, color)

    raise ValueError(f'{nick=} not found')
