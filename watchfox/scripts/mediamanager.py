#!/usr/bin/env python
import signal
from enum import StrEnum
from functools import partial
from typing import cast

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
)

from watchfox.obs import OBSManager, OBSMediaManager, make_obs_manager


class MediaControls(StrEnum):
    restart = 'restart'
    stop = 'stop'
    play = 'play'
    pause = 'pause'


def get_scenes(manager: OBSManager) -> list[str]:
    manager = make_obs_manager()
    data = manager.client.get_scene_list()
    data = cast(dict, data)
    return [d['sceneName'] for d in data['scenes']]


def get_sources(manager: OBSManager, scene: str) -> list[str]:
    data = manager.client.get_scene_item_list(scene)
    data = cast(dict, data)
    return [
        d['sourceName'] for d in data['sceneItems'] if d['inputKind'] == 'ffmpeg_source'
    ]


def get_media_sources(manager: OBSManager) -> list[str]:
    media_sources = []
    for scene in get_scenes(manager):
        media_sources.extend(get_sources(manager, scene))

    return sorted(set(media_sources))


def apply_media_control(manager: OBSMediaManager, control: MediaControls):
    if control is MediaControls.restart:
        manager.restart()
    elif control is MediaControls.play:
        manager.play()
    elif control is MediaControls.pause:
        manager.pause()
    elif control is MediaControls.stop:
        manager.stop()


class QMediaManagerWindow(QMainWindow):
    def __init__(self, manager: OBSManager, media_sources: list[str]):
        super().__init__()
        self._manager = manager
        self._media_sources = media_sources

        self.setWindowTitle('OBSMediaManager')
        self.setGeometry(0, 0, 100, 100)

        central = QWidget()
        layout = QGridLayout()
        central.setLayout(layout)

        for i, source in enumerate(media_sources):
            label = QLabel(source)
            layout.addWidget(label, i, 0)

            for j, media_control in enumerate(MediaControls):
                command = partial(
                    apply_media_control, manager.media(source), media_control
                )
                button = QPushButton(media_control)
                button.clicked.connect(command)
                layout.addWidget(button, i, j + 1)

        self.setCentralWidget(central)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    manager = make_obs_manager()
    media_sources = get_media_sources(manager)

    app = QApplication([])
    window = QMediaManagerWindow(manager, media_sources)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
