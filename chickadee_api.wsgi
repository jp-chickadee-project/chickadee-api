import os
import sys

sys.path.append('/home/michael/Documents/birdproject/chickadee-api')
from chickadee_api import create_app

application = app = create_app(os.environ.get('CHICK_CONFIG', 'production'))