from PhoenixNow.config import ProductionConfig, DevelopmentConfig
import os
from PhoenixNow import create_app

if os.environ.get('FLASK_DEBUG'):
    app = create_app(DevelopmentConfig)
else:
    app = create_app(ProductionConfig)
