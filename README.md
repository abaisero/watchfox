# watchfox
Connect to Minifoxwq server-sent-events to trigger python and OBS actions

---

## Requirements

Watchfox only supports Python >= 3.12, and requires Minifoxwq >= 0.8.

## Installation

It is advised to install this project in a new virtual environment, and to
install using edit-mode so that future pulled changes are used directly without
requiring reinstallation.

To install, clone this repo, (load your env) and run `python -m pip install -e .`.

## Configuration

To complete the configuration, edit `config.toml` and include your OBS
websocket server password under the `[connection]` section.  The password can
be found in `OBS -> Tools -> WebSocket Server Settings -> Show Connect Info`
(also make sure that the websocket server is enabled).

When using the default CLI, any field under the `[watchfox]` section will
become available in the event callbacks (see the example files);  you can use
use this to set up your own configuration data, e.g., this is where you would
put your foxwq username to determine which color you are playing.

---

## OBS

The OBSManager uses websockets to interface with the OBS instance.  Many
interactions are possible;  it is possible to read OBS settings, set OBS
settings, and even listen for OBS events.

However, for now, only few operations are implemented (e.g., media controls and
filter controls), based on my direct needs.  Feel free to open a github issue
to propose and request obs-related functionalities that are not yet
implemented.

---

## Audio

Watchfox also provides some functionality for playing audio clips directly
(without interacting with OBS).  This can be used for tts-like applications;
for now, there is a demo that reads out loud the moves as they are being
played.

As above, feel free to open a github issue to propose and request audio-related
functionalities that are not yet implemented.

---

## Examples

Check out the example files.  These can be taken as templates to implement your
own actions based on the server-sent-event stream.

### Default CLI Example

`example-default-cli.py` contains a template for getting started using the
default watchfox CLI.  The watchfox CLI provides subcommands to record and
replay Minifoxwq server-sent-events, and to run the full application.

The default CLI is useful to set up certain things automatically, and it allows
to record Minifoxwq events and replay them later which can help develop your
actions.  However, it is optional, and you can use any main script or CLI
framework you want, as long as you set up certain things manually.

### Custom CLI Example

`example-custom-cli.py` contains a template for getting started without using
the default watchfox CLI.  In this case, you will have to set up the event
stream, the obs instance, and any relevant configuration that you want to
become available in the callbacks yourself.

### Move TTS Example

`example-move-tts.py` contains a demo that employs TTS to verbalize the moves
obtained by the server-sent-event stream.  Before running it, you must first
generate the audio files by running `make-audio.py` (this will take a few
minutes).
