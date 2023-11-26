import logging
from typing import Any, Iterator

from blinker import Signal
from httpx_sse import ServerSentEvent

from watchfox.obs import OBSManager

logger = logging.getLogger(__name__)


event_names = [
    'match_start',
    'match_time',
    'match_move',
    'match_chat',
    'match_end',
]


class SSEProcessor:
    processing_start = Signal()
    processing_end = Signal()
    match_start = Signal()
    match_time = Signal()
    match_move = Signal()
    match_chat = Signal()
    match_end = Signal()

    signals = {
        'processing_start': processing_start,
        'processing_end': processing_end,
        'match_start': match_start,
        'match_time': match_time,
        'match_move': match_move,
        'match_chat': match_chat,
        'match_end': match_end,
    }

    def __init__(self, manager: OBSManager, config: dict[str, Any] | None = None):
        super().__init__()
        self.manager = manager
        self.config = {} if config is None else config

    def process_events(self, events: Iterator[ServerSentEvent]):
        self.processing_start.send(self)

        for event in events:
            logger.info(f'processing SSE {event.event}')
            self.process_event(event)

        self.processing_end.send(self)

    def process_event(self, event: ServerSentEvent):
        name = event.event
        data = event.json()

        if name == 'match_move':
            # convert json list into tuple
            data['move'] = tuple(data['move'])

        try:
            signal = self.signals[name]
        except KeyError:
            logger.error(f'invalid event {name=}')
        else:
            signal.send(self, data=data)
