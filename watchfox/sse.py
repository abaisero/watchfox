import logging
import pickle
import tomllib
from contextlib import contextmanager
from typing import Iterator, cast

import httpx
from httpx_sse import EventSource, ServerSentEvent, connect_sse

logger = logging.getLogger('__name__')


@contextmanager
def make_event_source(url: str) -> Iterator[EventSource]:
    with httpx.Client(timeout=None) as client:
        try:
            with connect_sse(client, 'GET', url) as event_source:
                yield event_source
        except (httpx.ConnectError, httpx.ReadError) as error:
            logger.exception(error)
            logger.error('This probably means `minifox` is not running')
            exit(1)


def server_sent_events(url: str | None = None) -> Iterator[ServerSentEvent]:
    if url is None:
        with open('config.toml', 'rb') as f:
            config = tomllib.load(f)

        url = cast(str, config['minifoxwq']['sse_url'])

    with make_event_source(url) as event_source:
        yield from event_source.iter_sse()


def record_events(filename: str, append: bool, events: Iterator[ServerSentEvent]):
    mode = 'ab' if append else 'wb'
    with open(filename, mode) as f:
        for event in events:
            pickle.dump(event, f)


def get_recorded_events(filename: str) -> Iterator[ServerSentEvent]:
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
