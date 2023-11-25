#!/usr/bin/env python
import logging
import logging.config
import tomllib

import click

from watchfox.minifox import SSEProcessor, event_names
from watchfox.obs import make_obs_manager
from watchfox.sse import get_recorded_events, record_events, server_sent_events
from watchfox.utils import sleep_iterator

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
@click.option(
    '--config',
    'config_filename',
    type=click.Path(exists=True, dir_okay=False),
    default='config.toml',
)
@click.option(
    '--log/--no-log',
    is_flag=True,
    help='Register logging info.',
)
@click.option(
    '--log-config',
    'log_config_filename',
    type=click.Path(exists=True, dir_okay=False),
    default='logging.toml',
)
def cli(
    context: click.Context,
    config_filename: str,
    log: bool,
    log_config_filename: str,
):
    with open(config_filename, 'rb') as f:
        context.obj = tomllib.load(f)

    if log:
        try:
            with open(log_config_filename, 'rb') as f:
                logging_config = tomllib.load(f)
        except FileNotFoundError:
            print(f'logging file `{log_config_filename}` not found.  skipping.')
        else:
            logging.config.dictConfig(logging_config)


@cli.command('record')
@click.pass_obj
@click.argument('events-filename', default='events.pk')
@click.option('--append', is_flag=True, help='Append server-sent events to file.')
def cmd_record(config: dict, events_filename: str, append: bool):
    """Record events from minifox."""
    print(f'command record {events_filename=}')

    url = config['minifoxwq']['sse_url']
    events = server_sent_events(url)
    record_events(events_filename, append, events)


@cli.command('replay')
@click.pass_obj
@click.argument(
    'events-filename',
    type=click.Path(exists=True, dir_okay=False),
    default='events.pk',
)
@click.option(
    '--whitelist',
    type=click.Choice(event_names),
    multiple=True,
    help='Only process these events.',
)
@click.option(
    '--blacklist',
    type=click.Choice(event_names),
    multiple=True,
    help='Do not process these events.',
)
@click.option('--sleep', type=float, default=1.0, help='Seconds between events.')
@click.option('--mock-obs', is_flag=True, help='Do not connect to OBS instance.')
def cmd_replay(
    config: dict,
    events_filename: str,
    whitelist: tuple[str],
    blacklist: tuple[str],
    sleep: float,
    mock_obs: bool,
):
    """Process pre-recorded events."""
    print(f'command replay {events_filename=}')

    events = get_recorded_events(events_filename)
    if whitelist:
        events = (event for event in events if event.event in whitelist)
    events = (event for event in events if event.event not in blacklist)
    events = sleep_iterator(events, sleep)

    manager = make_obs_manager(mock=mock_obs)
    processor = SSEProcessor(manager, config.get('watchfox'))
    processor.process_events(events)


@cli.command('run')
@click.pass_obj
@click.option('--mock-obs', is_flag=True, help='Do no connect to OBS instance.')
def cmd_run(config: dict, mock_obs: bool):
    """Process live events coming from minifox."""
    print('command run')

    url = config['minifoxwq']['sse_url']
    events = server_sent_events(url)

    manager = make_obs_manager(mock=mock_obs)
    processor = SSEProcessor(manager, config.get('watchfox'))
    processor.process_events(events)
