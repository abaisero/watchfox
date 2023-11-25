#!/usr/bin/env python

import asyncio
import itertools as itt
import string

import edge_tts

LETTERS = list(string.ascii_uppercase[:19])
NUMBERS = list(range(1, 20))


def make_text(color: str, row: int, col: int):
    """Make corresponding audio text, e.g., `black plays C 4`."""
    if row == -1 and col == -1:
        return f'{color} passes'

    if 0 <= row < 19 and 0 <= col < 19:
        number = NUMBERS[row]
        letter = LETTERS[col]

        # edge-tts pronounces `A` as an article, not as a letter;  replacing with `hay`
        if letter == 'A':
            letter = 'hay'

        return f'{color} plays {letter} {number}'

    raise ValueError(f'invalid inputs {color=} {row=} {col=}')


async def save_audio(text: str, filename: str):
    print(f'saving {text=} into {filename=}')
    communicate = edge_tts.Communicate(text)
    await communicate.save(filename)


COLORS = ['white', 'black']
COORDINATES = itt.chain(
    [(-1, -1)],
    itt.product(range(19), range(19)),
)


async def main():
    for color, (row, col) in itt.product(COLORS, COORDINATES):
        text = make_text(color, row, col)
        filename = f'audio/{color}.{row}.{col}.mp3'
        await save_audio(text, filename)


if __name__ == '__main__':
    asyncio.run(main())
