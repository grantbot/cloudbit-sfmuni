import json
import logging
import logging.config

import cherrypy

from log_conf import LOG_CONF

logging.config.dictConfig(LOG_CONF)
LOGGER = logging.getLogger(__name__)

class SfMuni(object):

    exposed = True

    def POST(self, **kwargs):
        body = json.loads(cherrypy.request.body.read())
        LOGGER.info('BODY: %s', body)
        return 'POSTED'


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5000,
                            'log.screen': False,
                            'log.access_file': '',
                            'log.error_file': '',
                            })
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

    cherrypy.tree.mount(
        SfMuni(), '/api/hello',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()
