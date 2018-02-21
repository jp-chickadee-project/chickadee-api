
from flask_script import Manager
import unittest

from chickadee_api import create_app

manager = Manager(create_app)

@manager.command
def test():
	tests = unittest.TestLoader().discover('test', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1

if __name__ == "__main__":
    manager.run()