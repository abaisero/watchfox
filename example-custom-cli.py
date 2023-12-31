#!/usr/bin/env python
from watchfox.minifox import SSEProcessor
from watchfox.obs import OBSManager, make_obs_manager
from watchfox.sse import server_sent_events
from watchfox.types import (
    MinifoxMatchChat,
    MinifoxMatchEnd,
    MinifoxMatchMove,
    MinifoxMatchStart,
    MinifoxMatchTime,
)


@SSEProcessor.match_start.connect
def on_match_start(processor: SSEProcessor, data: MinifoxMatchStart):
    print(f'Event: match_time for game with {data['id']=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media.restart('name-of-media')

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_time.connect
def on_match_time(processor: SSEProcessor, data: MinifoxMatchTime):
    print(f'Event: match_time for game with {data['id']=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media.restart('name-of-media')

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_move.connect
def on_match_move(processor: SSEProcessor, data: MinifoxMatchMove):
    print(f'Event: match_time for game with {data['id']=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media.restart('name-of-media')

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_chat.connect
def on_match_chat(processor: SSEProcessor, data: MinifoxMatchChat):
    print(f'Event: match_time for game with {data['id']=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media.restart('name-of-media')

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


@SSEProcessor.match_end.connect
def on_match_end(processor: SSEProcessor, data: MinifoxMatchEnd):
    print(f'Event: match_time for game with {data['id']=}')

    # we can access the obs manager
    assert isinstance(processor.manager, OBSManager)
    # e.g., processor.manager.media.restart('name-of-media')

    # we can access config data
    assert processor.config['config-key'] == 'config-value'


if __name__ == '__main__':
    # we can set up out own cli here, using argparse or other tools

    # connects to real minifox
    events = server_sent_events()

    # uses a mock obs manager
    manager = make_obs_manager(mock=True)

    # processes events
    processor = SSEProcessor(manager, {'config-key': 'config-value'})
    processor.process_events(events)
