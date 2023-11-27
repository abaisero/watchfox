import logging
from queue import Queue
from threading import Thread

import playsound

from watchfox.types import Color, CoordinateSystem
from watchfox.utils import make_move_audio_filename

logger = logging.getLogger(__name__)


type audiotask = str | None
queue: Queue[audiotask]
thread: Thread | None = None


def play_audio_target(queue: Queue[str | None]):
    while True:
        filename = queue.get()
        if filename is None:
            break

        logger.debug(f'playing {filename}')
        playsound.playsound(filename)


def play_audio(filename: str):
    global thread, queue

    if thread is None:
        logger.debug('creating audio queue')
        queue = Queue()

        logger.debug('creating audio thread')
        thread = Thread(target=play_audio_target, args=(queue,), daemon=True)
        thread.start()

    logger.info(f'sending `{filename}` to play queue')
    queue.put_nowait(filename)


def join_audio():
    if thread is None:
        return

    queue.put_nowait(None)
    thread.join()


def play_move_audio(system: CoordinateSystem, color: Color, move: tuple[int, int]):
    filename = make_move_audio_filename(system, color, move)
    play_audio(filename)
