"""Module for /api/muni"""

import logging
import time
import threading

import cherrypy

from services.muni import muni
from services.cloudbit import cloudbit

LOGGER = logging.getLogger()
ROUTE = '5'
STOP_NAME = 'market_1st'
DIRECTION = 'inbound'
NUM_BUSES = 3


class SfMuni(object):

    exposed = True

    @cherrypy.tools.json_in()
    def POST(self, **kwargs):
        LOGGER.info('Got POST request.')
        # This route should only be subscribed to amplitude:delta:ignite
        # (button press)
        body = cherrypy.request.json
        LOGGER.debug('POST body: %s', body)
        bit_id = body['bit_id']

        # Get muni prediction
        try:
            next_buses = muni.get_next(route=ROUTE,
                                       stop_name=STOP_NAME,
                                       direction=DIRECTION,
                                       num=NUM_BUSES)
        except muni.NoPredictionsError:
            LOGGER.info('Sweeping face.')
            cloudbit.Motions.sweep_face(bit_id)
            return 'No prediction.'

        except KeyError:
            LOGGER.info('Harlem shake-ing.')
            cloudbit.Motions.harlem_shake(bit_id)
            return 'You gave bad input.'

        except Exception as err:
            LOGGER.exception('NextBus API flaked: %s', err)
            cloudbit.Motions.harlem_shake(bit_id)
            return 'NextBus API call failed.'

        thread = threading.Thread(target=async_cloudbit_output,
                                  args=(bit_id, next_buses, 3))

        LOGGER.info('Spawning new thread.')
        thread.start()

        LOGGER.info('Responding to POST.')
        return '{route} at {stop_name} {direction} in {next_buses}' \
            .format(route=ROUTE,
                    stop_name=STOP_NAME,
                    direction=DIRECTION,
                    next_buses=next_buses)


def async_cloudbit_output(bit_id, next_buses, delay):
    """Iterate over bus times and hit CloudBit with the right output voltages.

    Adds a delay between each output call, to avoid stuttering.

    Arguments:
        bit_id (str) Unique identifier of the target CloudBit
        next_buses ([int]) List of bus wait times
        delay (int) time to wait between CloudBit output calls (seconds)
    """
    for bus_wait in next_buses:
        if bus_wait <= 1:
            LOGGER.info('Ur not gonna make the next one.')

        else:
            # Calculate voltage with response
            volts_prcnt = cloudbit.get_percentage(bus_wait)

            # Hit cloudbit
            cloudbit.output_to_servo(bit_id, volts_prcnt, delay * 1000)
            time.sleep(delay)
