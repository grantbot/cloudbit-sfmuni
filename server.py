import logging

import cherrypy

LOGGER = logging.getLogger('CLOUDBIT_SFMUNI')

class SfMuni(object):
    exposed = True

    def GET(self):
        return 'HELLO WORLD'

    def POST(self, **kwargs):

        LOGGER.info('request.body_params: %s', cherrypy.request.body_params)
        LOGGER.info('request.params: %s', cherrypy.request.params)
        return 'POSTED'


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5000})
    cherrypy.tree.mount(
        SfMuni(), '/api/hello',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()
