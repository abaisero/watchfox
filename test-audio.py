#!/usr/bin/env python
from watchfox.audio import join_audio, play_move_audio

play_move_audio('fox', 'black', (-1, -1))
play_move_audio('fox', 'black', (1, 2))

play_move_audio('ogs', 'black', (-1, -1))
play_move_audio('ogs', 'black', (1, 2))

play_move_audio('ogs', 'black', (-1, -1))
play_move_audio('ogs', 'black', (1, 2))

join_audio()
