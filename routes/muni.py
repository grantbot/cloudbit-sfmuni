"""Module for /api/muni"""

import logging

import cherrypy

from services.muni import muni
from services.cloudbit import cloudbit

LOGGER = logging.getLogger()


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
            first, second = muni.get_next_two(route='5',
                                              stop_name='market_1st',
                                              direction='inbound')
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

        # Not gonna make it
        if first <= 1:
            LOGGER.info('Ur not gonna make it.')
            first = second

        # Calculate voltage with response
        volts_prcnt = cloudbit.get_percentage(first)

        # Hit cloudbit
        res = cloudbit.output_to_servo(bit_id, volts_prcnt, 4000)

        return str(first)
