#!/usr/bin/env python
import logging
import asyncio

from watchfox.audio import play_move_audio
from watchfox.minifox import SSEProcessor
from watchfox.obs import make_obs_manager
from watchfox.sse import aget_events
from watchfox.types import MinifoxMatchMove

logger = logging.getLogger(__name__)


@SSEProcessor.match_move.connect
async def on_match_move(_: SSEProcessor, data: MinifoxMatchMove):
    color = 'white' if data.move_number % 2 == 0 else 'black'

    logger.info(f'{color=} {data.move=}, playing audio')
    play_move_audio('fox', color, data.move)


if __name__ == '__main__':
    # connects to real minifox
    events = aget_events()

    # uses a mock obs manager
    manager = make_obs_manager(mock=True)

    # processes events
    processor = SSEProcessor(manager)
    asyncio.run(processor.process(events))
