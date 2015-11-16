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
            next_three = muni.get_next(route='5',
                                       stop_name='market_1st',
                                       direction='inbound',
                                       num=3)
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

        for bus_wait in next_three:
            if bus_wait <= 1:
                LOGGER.info('Ur not gonna make the next one.')

            else:
                # Calculate voltage with response
                volts_prcnt = cloudbit.get_percentage(bus_wait)

                # Hit cloudbit
                cloudbit.output_to_servo(bit_id, volts_prcnt, 3000)

        return str(next_three)
