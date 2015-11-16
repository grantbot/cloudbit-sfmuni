"""Module for interacting with the nextbus API."""

import logging

import requests
import xmltodict

from services.muni.stop_map import STOP_MAP

LOGGER = logging.getLogger()

NEXTBUS_URL = """ \
    http://webservices.nextbus.com/service/publicXMLFeed? \
        command={command} \
        &a=sf-muni \
        &r={route} \
        &s={stop_tag} \
"""


def get_next_two(route, stop_name, direction):
    """Get the next predicted bus wait time, in minutes."""
    command = 'predictions'

    # Get stop tag
    try:
        stop_tag = STOP_MAP[route][stop_name][direction]
    except KeyError:
        LOGGER.warn('Invalid route, stop_name, or direction')
        raise

    # Insert URL params and send GET
    url = NEXTBUS_URL.format(command=command,
                             route=route,
                             stop_tag=stop_tag) \
                     .replace(' ', '')

    LOGGER.info('Hitting NextBus.')
    res = requests.get(url)

    # XML to dict
    parsed = xmltodict.parse(res.text)

    # 'direction' won't exist inside 'predictions' if no predictions
    try:
        predictions = parsed['body'] \
                            ['predictions'] \
                            ['direction'] \
                            ['prediction']
    except KeyError:
        LOGGER.info('No predictions.')
        LOGGER.debug('Parsed XML: %s', parsed)
        raise NoPredictionsError

    first, second = extract_minutes(predictions)

    LOGGER.info('Next {direction} {route} in: {first} and {second} min'
                .format(direction=direction,
                        route=route,
                        first=first,
                        second=second))

    return first, second


def extract_minutes(predictions):
    """Pull the earliest two predictions, in minutes, from parsed NextBus XML."""
    times = sorted([int(p['@minutes']) for p in predictions])
    return times[0], times[1]


# CUSTOM EXCEPTIONS
class NoPredictionsError(Exception):
    pass

