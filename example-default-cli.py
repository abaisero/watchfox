#!/usr/bin/env python
import logging

from watchfox.cli import cli
from watchfox.minifox import SSEProcessor
from watchfox.obs import OBSManager
from watchfox.types import (
    MinifoxMatchChat,
    MinifoxMatchEnd,
    MinifoxMatchMove,
    MinifoxMatchStart,
    MinifoxMatchTime,
)

logger = logging.getLogger(__name__)


@SSEProcessor.processing_start.connect
async def on_processing_start(processor: SSEProcessor):
    print('Processing is starting')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.processing_end.connect
async def on_processing_end(processor: SSEProcessor):
    print('Processing is ending')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_start.connect
async def on_match_start(processor: SSEProcessor, data: MinifoxMatchStart):
    print(f'Event: match_start for game with {data.id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_time.connect
async def on_match_time(processor: SSEProcessor, data: MinifoxMatchTime):
    print(f'Event: match_time for game with {data.id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_move.connect
async def on_match_move(processor: SSEProcessor, data: MinifoxMatchMove):
    print(f'Event: match_move for game with {data.id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_chat.connect
async def on_match_chat(processor: SSEProcessor, data: MinifoxMatchChat):
    print(f'Event: match_chat for game with {data.id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_end.connect
async def on_match_end(processor: SSEProcessor, data: MinifoxMatchEnd):
    print(f'Event: match_end for game with {data.id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


if __name__ == '__main__':
    cli()
