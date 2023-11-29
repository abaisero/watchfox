import logging
import pickle
import tomllib
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Callable, Iterator, cast

import httpx
from httpx_sse import EventSource, ServerSentEvent, aconnect_sse, connect_sse

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


@asynccontextmanager
async def amake_event_source(url: str) -> AsyncIterator[EventSource]:
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            async with aconnect_sse(client, 'GET', url) as event_source:
                yield event_source
        except (httpx.ConnectError, httpx.ReadError) as error:
            logger.exception(error)
            logger.error('This probably means `minifox` is not running')
            exit(1)


def get_config_sse_url() -> str:
    with open('config.toml', 'rb') as f:
        config = tomllib.load(f)

    return cast(str, config['minifoxwq']['sse_url'])


def get_events(url: str | None = None) -> Iterator[ServerSentEvent]:
    if url is None:
        url = get_config_sse_url()

    with make_event_source(url) as event_source:
        yield from event_source.iter_sse()


async def aget_events(url: str | None = None) -> AsyncIterator[ServerSentEvent]:
    if url is None:
        url = get_config_sse_url()

    async with amake_event_source(url) as event_source:
        async for event in event_source.aiter_sse():
            yield event


type Recorder[T] = Callable[[T], None]


@contextmanager
def event_recorder(filename: str, append: bool) -> Iterator[Recorder[ServerSentEvent]]:
    mode = 'ab' if append else 'wb'
    with open(filename, mode) as f:
        yield lambda event: pickle.dump(event, f)


def get_recorded_events(filename: str) -> Iterator[ServerSentEvent]:
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
