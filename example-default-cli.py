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


@SSEProcessor.match_start.connect
def on_match_start(processor: SSEProcessor, data: MinifoxMatchStart):
    id = data['id']
    print(f'Event: match_start for game with {id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_time.connect
def on_match_time(processor: SSEProcessor, data: MinifoxMatchTime):
    id = data['id']
    print(f'Event: match_time for game with {id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_move.connect
def on_match_move(processor: SSEProcessor, data: MinifoxMatchMove):
    id = data['id']
    print(f'Event: match_move for game with {id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_chat.connect
def on_match_chat(processor: SSEProcessor, data: MinifoxMatchChat):
    id = data['id']
    print(f'Event: match_chat for game with {id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_end.connect
def on_match_end(processor: SSEProcessor, data: MinifoxMatchEnd):
    id = data['id']
    print(f'Event: match_end for game with {id=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media('name-of-media').restart()

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


if __name__ == '__main__':
    cli()
