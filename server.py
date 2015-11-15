import json

import cherrypy

from routes.muni import SfMuni


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
