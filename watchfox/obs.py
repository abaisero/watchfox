from __future__ import annotations

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
    def __init__(self, client: OBSClient, source: str, filter: str):
        super().__init__()
        self.client = client
        self.source = source
        self.filter = filter

    @property
    def enabled(self) -> bool:
        data = self.client.get_source_filter(self.source, self.filter)
        data = cast(dict, data)
        return data['filterEnabled']

    @enabled.setter
    def enabled(self, enabled: bool):
        logger.info(f'setting {self.source=} {self.filter=} {enabled=}')
        self.client.set_source_filter_enabled(self.source, self.filter, enabled)

    @property
    def settings(self) -> dict:
        data = self.client.get_source_filter(self.source, self.filter)
        data = cast(dict, data)
        return data['filterSettings']

    @settings.setter
    def settings(self, settings: dict):
        self.client.set_source_filter_settings(self.source, self.filter, settings, True)


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
    def __init__(self, client: OBSClient, media: str):
        super().__init__()
        self.client = client
        self.media = media

    def play(self):
        logger.info(f'playing {self.media=}')
        self.client.trigger_media_input_action(
            self.media,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY',
        )

    def pause(self):
        logger.info(f'pausing {self.media=}')
        self.client.trigger_media_input_action(
            self.media,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE',
        )

    def stop(self):
        logger.info(f'stopping {self.media=}')
        self.client.trigger_media_input_action(
            self.media,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP',
        )

    def restart(self):
        logger.info(f'restarting {self.media=}')
        self.client.trigger_media_input_action(
            self.media,
            'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART',
        )


class OBSSceneManager:
    def __init__(self, client: OBSClient, scene: str):
        super().__init__()
        self.client = client
        self.scene = scene

    def item(self, source: str) -> OBSSceneItemManager:
        return OBSSceneItemManager(self.client, self.scene, source)

    def preview(self):
        logger.info(f'setting {self.scene=} as preview')
        self.client.set_current_preview_scene(self.scene)

    def program(self):
        logger.info(f'setting {self.scene=} as program')
        self.client.set_current_program_scene(self.scene)


class OBSSceneItemManager:
    def __init__(self, client: OBSClient, scene: str, source: str):
        super().__init__()
        self.client = client
        self.scene = scene
        self.source = source
        self.source_id = self._get_source_id()

    def _get_source_id(self):
        data = self.client.get_scene_item_id(self.scene, self.source)
        data = cast(dict, data)
        return data['sceneItemId']

    @property
    def enabled(self) -> bool:
        data = self.client.get_scene_item_enabled(self.scene, self.source_id)
        data = cast(dict, data)
        return data['sceneItemEnabled']

    @enabled.setter
    def enabled(self, enabled: bool):
        logger.info(f'setting {self.scene=} {self.source=} {enabled=}')
        self.client.set_scene_item_enabled(self.scene, self.source_id, enabled)

    @property
    def locked(self) -> bool:
        data = self.client.get_scene_item_locked(self.scene, self.source_id)
        data = cast(dict, data)
        return data['sceneItemLocked']

    @locked.setter
    def locked(self, locked: bool):
        logger.info(f'setting {self.scene=} {self.source=} {locked=}')
        self.client.set_scene_item_locked(self.scene, self.source_id, locked)


class OBSSourceManager:
    def __init__(self, client: OBSClient, source: str):
        super().__init__()
        self.client = client
        self.source = source

    def filter(self, filter: str) -> OBSFilterManager:
        return OBSFilterManager(self.client, self.source, filter)


class OBSLabelManager:
    def __init__(self, client: OBSClient, label: str):
        super().__init__()
        self.client = client
        self.label = label

    @property
    def text(self) -> str:
        data = self.client.get_input_settings(self.label)
        data = cast(dict, data)
        return data['inputSettings']['text']

    @text.setter
    def text(self, text: str):
        logger.info(f'setting {self.label=} {text=}')
        settings = {'text': text}
        self.client.set_input_settings(self.label, settings, True)


class OBSManager:
    # Protocols
    # https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
    def __init__(self, client: OBSClient):
        super().__init__()
        self.client = client

    def media(self, media: str) -> OBSMediaManager:
        return OBSMediaManager(self.client, media)

    def hotkey(self) -> OBSHotkeyManager:
        return OBSHotkeyManager(self.client)

    def filter(self, source: str, filter: str) -> OBSFilterManager:
        return OBSFilterManager(self.client, source, filter)

    def label(self, label: str) -> OBSLabelManager:
        return OBSLabelManager(self.client, label)

    def scene(self, scene: str) -> OBSSceneManager:
        return OBSSceneManager(self.client, scene)

    def scene_item(self, scene: str, source: str) -> OBSSceneItemManager:
        return OBSSceneItemManager(self.client, scene, source)

    def source(self, source: str) -> OBSSourceManager:
        return OBSSourceManager(self.client, source)


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
