#!/usr/bin/env python
import logging

from watchfox.audio import play_audio
from watchfox.minifox import SSEProcessor
from watchfox.obs import make_obs_manager
from watchfox.sse import server_sent_events
from watchfox.types import MinifoxMatchMove

logger = logging.getLogger(__name__)


@SSEProcessor.match_move.connect
def on_match_move(_: SSEProcessor, data: MinifoxMatchMove):
    player = 'white' if data['move_number'] % 2 == 0 else 'black'
    row, col = data['move']

    logger.info(f'{player=} {row=} {col=}, playing audio')
    filename = f'audio/{player}.{row}.{col}.mp3'
    play_audio(filename)


if __name__ == '__main__':
    # connects to real minifox
    events = server_sent_events()

    # uses a mock obs manager
    manager = make_obs_manager(mock=True)

    # processes events
    processor = SSEProcessor(manager)
    processor.process_events(events)
