"""Module for interacting with Cloudbit devices."""

import logging
import os

import requests


LOGGER = logging.getLogger()

LITTLEBITS_OUTPUT_URL = 'https://api-http.littlebitscloud.cc/devices/{bit_id}/output'
LITTLEBITS_TOKEN = os.getenv('LITTLEBITS_TOKEN')
AUTH_HEADER = {'Authorization': 'Bearer ' + LITTLEBITS_TOKEN}
MAX_MINUTES = 20  # Can be bigger if servo has larger ROM


class Motions(object):
    """Namespace for convenience methods that map to specific servo motions."""

    @staticmethod
    def sweep_face(bit_id):
        """A quick, full-range-of-motion sweep."""
        output_to_servo(bit_id, 100, 400)

    @staticmethod
    def harlem_shake(bit_id):
        """Two short, quick shakes."""
        output_to_servo(bit_id, 50, 100)
        output_to_servo(bit_id, 50, 100)


def output_to_servo(bit_id, volts_prcnt, duration_ms):
    """Send a voltage and duration to specific bit_id.

    Arguments:
        bit_id (str) Unique identifier of the target CloudBit
        volts_prcnt (int between [0, 100]) percentage of output device voltage
        duration_ms (int) milliseconds for which to sustain output voltage
    """
    url = LITTLEBITS_OUTPUT_URL.format(bit_id=bit_id)

    output_data = {
        'percent': volts_prcnt,
        'duration_ms': duration_ms
    }

    LOGGER.info('Outputting to cloudbit: %s', output_data)
    res = requests.post(url,
                        headers=AUTH_HEADER,
                        data=output_data)
    return res


def get_percentage(part, whole=MAX_MINUTES):
    """Calculate a percentage of two numbers, defaulting to whatever value we
    consider to be the 'max' output.
    """
    if part >= whole:
        return 100

    result = int(100 * part / whole)

    LOGGER.debug('{part} is {result} percent of {whole}'
                .format(part=part,
                        result=result,
                        whole=whole))
    return result







