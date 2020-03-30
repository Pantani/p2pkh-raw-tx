import sys
import unittest
from app import blueprint
from flask_script import Manager
from app.api import start_app

""" Verify the python version """
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required.\n')
    sys.exit(1)

app = start_app()
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)


@manager.command
def run():
    """
    Runs the application.
    """
    app.run()


@manager.command
def test():
    """
    Runs the unit tests.
        :return: int as 0 is a success or 1 if fails.
    """
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
