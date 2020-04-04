import sys

from app import blueprint
from flask_script import Manager
from app.api import start_app
from app.api.config import ProductionConfig

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
    app.run(debug=ProductionConfig.DEBUG, port=ProductionConfig.PORT, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
