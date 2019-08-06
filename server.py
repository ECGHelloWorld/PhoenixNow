import wsgiserver
from PhoenixNow.config import ProductionConfig, DevelopmentConfig
from PhoenixNow.factory import create_app, extensions, app
import os

if os.environ.get('FLASK_DEBUG'):
    create_app(DevelopmentConfig)
    extensions()
else:
    create_app(ProductionConfig)
    extensions()

http_server = wsgiserver.WSGIServer(app, port=5000)
http_server.start()