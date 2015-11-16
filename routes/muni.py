"""Module for /api/muni"""

import logging

import cherrypy


LOGGER = logging.getLogger()


class SfMuni(object):

    exposed = True

    @cherrypy.tools.json_in()
    def POST(self, **kwargs):
        # Validate user and bit_id
        body = cherrypy.request.json
        LOGGER.info('BODY: %s', body['bit_id'])
        # Validate delta:ignite, voltage percent
        # muni.get_next(route= , stop_name=, direction=)
        # Calculate voltage with response
        # Hit cloudbit
        return 'POSTED'
