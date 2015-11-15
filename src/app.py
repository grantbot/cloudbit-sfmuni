import logging

import cherrypy

LOGGER = logging.getLogger('CLOUDBIT_SFMUNI')

class HelloWorld(object):
    exposed = True

    def POST(self, **kwargs):

        LOGGER.info('request.body_params: %s', cherrypy.request.body_params)
        LOGGER.info('request.params: %s', cherrypy.request.params)
        return 'POSTED'


if __name__ == '__main__':
    cherrypy.tree.mount(
        HelloWorld(), '/api/hello',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
