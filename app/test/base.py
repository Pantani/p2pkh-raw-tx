from flask_testing import TestCase
from manage import app


class BaseTestCase(TestCase):
    """
    Base Tests
    """

    def create_app(self):
        app.config.from_object('app.api.config.TestingConfig')
        return app
