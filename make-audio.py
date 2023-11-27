#!/usr/bin/env python

import argparse
import asyncio
import itertools as itt
import os
import string

import edge_tts

from watchfox.types import Color, CoordinateSystem
from watchfox.utils import make_move_audio_filename


def make_text(
    color: Color,
    row: int,
    col: int,
    rowmap: list,
    colmap: list,
) -> str:
    """Make corresponding audio text, e.g., `black plays C 4`."""
    if row == -1 and col == -1:
        return f'{color} passes'

    if 0 <= row < 19 and 0 <= col < 19:
        number = rowmap[row]
        letter = colmap[col]

        # edge-tts pronounces `A` as an article, not as a letter;  replacing with `hay`
        if letter == 'A':
            letter = 'hay'

        return f'{color} plays {letter} {number}'

    raise ValueError(f'invalid inputs {color=} {row=} {col=}')


async def save_audio(text: str, filename: str):
    print(f'saving {text=} into {filename=}')
    communicate = edge_tts.Communicate(text)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    await communicate.save(filename)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('systems', choices=['fox', 'ogs', 'kgs'], nargs='+')
    return parser.parse_args()


def make_movemaps(system: CoordinateSystem) -> tuple[list, list]:
    if system == 'fox':
        LETTERS = list(string.ascii_uppercase[:19])
        NUMBERS = list(range(1, 20))
        return NUMBERS, LETTERS

    if system == 'ogs':
        LETTERS = list(string.ascii_uppercase[:20])
        LETTERS.remove('I')
        NUMBERS = list(reversed(range(1, 20)))
        return NUMBERS, LETTERS

    if system == 'kgs':
        LETTERS = list(string.ascii_uppercase[:20])
        LETTERS.remove('I')
        NUMBERS = list(reversed(range(1, 20)))
        return NUMBERS, LETTERS

    raise ValueError(f'invalid {system=}')


COLORS: list[Color] = ['white', 'black']
MOVES = itt.chain(
    [(-1, -1)],
    itt.product(range(19), range(19)),
)


async def main(args):
    # TODO: implement using async tasks

    # remove duplicates while maintaining order
    systems = list(dict.fromkeys(args.systems))
    for system in systems:
        rowmap, colmap = make_movemaps(system)

        for color, (row, col) in itt.product(COLORS, MOVES):
            text = make_text(color, row, col, rowmap, colmap)
            filename = make_move_audio_filename(system, color, (row, col))
            await save_audio(text, filename)


if __name__ == '__main__':
    args = parse_args()
    asyncio.run(main(args))
