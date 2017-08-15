from gevent.wsgi import WSGIServer
from PhoenixNow.config import ProductionConfig, DevelopmentConfig
from PhoenixNow.factory import create_app, extensions
import os

if os.environ.get('FLASK_DEBUG'):
    app = extensions(create_app(DevelopmentConfig))
else:
    app = extensions(create_app(ProductionConfig))

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()