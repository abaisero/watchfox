import logging
from typing import cast
from unittest.mock import Mock

from obsws_python import ReqClient

logger = logging.getLogger(__name__)


class OBSClient(ReqClient):
    def send(self, *args, **kwargs) -> dict:
        data = super().send(*args, **kwargs, raw=True)
        return cast(dict, data)


class OBSFilterManager:
    def __init__(self, client: OBSClient):
        super().__init__()
        self.client = client

    def enable(self, source: str, filter: str):
        logger.info(f'enabling {source=} {filter=}')
        self.client.set_source_filter_enabled(source, filter, True)

    def disable(self, source: str, filter: str):
        logger.info(f'enabling {source=} {filter=}')
        self.client.set_source_filter_enabled(source, filter, False)


class OBSHotkeyManager:
    def __init__(self, client: OBSClient):
        super().__init__()
        self.client = client

    def trigger_by_name(self, name: str):
        logger.info(f'triggering hotkey {name=}')
        self.client.trigger_hotkey_by_name(name)

    def trigger_by_keys(
        self,
        key: str,
        *,
        shift=False,
        ctrl=False,
        alt=False,
        cmd=False,
    ):
        # https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h
        logger.info(f'triggering hotkey {shift=} {ctrl=} {alt=} {cmd=} {key=}')
        self.client.trigger_hotkey_by_key_sequence(key, shift, ctrl, alt, cmd)


class OBSMediaManager:
    def __init__(self, client: OBSClient):
        super().__init__()
        self.client = client

    def play(self, name: str):
        logger.info(f'playing media {name=}')
        self.client.trigger_media_input_action(
            name,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY',
        )

    def pause(self, name: str):
        logger.info(f'pausing media {name=}')
        self.client.trigger_media_input_action(
            name,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE',
        )

    def stop(self, name: str):
        logger.info(f'stopping media {name=}')
        self.client.trigger_media_input_action(
            name,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP',
        )

    def restart(self, name: str):
        logger.info(f'restarting media {name=}')
        self.client.trigger_media_input_action(
            name,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART',
        )


class OBSManager:
    # Protocols
    # https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
    def __init__(self, client: OBSClient):
        super().__init__()
        self.client = client

    @property
    def media(self) -> OBSMediaManager:
        return OBSMediaManager(self.client)

    @property
    def hotkey(self) -> OBSHotkeyManager:
        return OBSHotkeyManager(self.client)

    @property
    def filter(self) -> OBSFilterManager:
        return OBSFilterManager(self.client)


def make_obs_manager(*, mock: bool = False) -> OBSManager:
    if mock:
        return Mock()

    try:
        logger.info('making obs client')
        client = OBSClient()
    except ConnectionRefusedError as error:
        logger.exception(error)
        logger.error('This probably means `obs` is not running')
        exit(1)

    return OBSManager(client)
