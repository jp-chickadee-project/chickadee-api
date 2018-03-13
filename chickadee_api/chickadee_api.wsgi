import os
import sys

sys.path.append('/srv/http/chickadee-api')
from chickadee_api import create_app

application = app = create_app(os.environ.get('CHICK_CONFIG', 'production'))