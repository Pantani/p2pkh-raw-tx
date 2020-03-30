import unittest

from flask_testing import TestCase

from manage import app


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.api.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(app.config['PORT'], 5000)
        self.assertEqual(app.config['MIN_FEE'], 1000)
        self.assertEqual(app.config['NETWORK'], 'testnet')
        self.assertEqual(app.config['API_URLAPI_URL'], 'https://testnet.blockchain.info')
        self.assertEqual(app.config['CONFIRMATIONS'], 6)
        self.assertEqual(app.config['MIN_CHANGE_VALUE'], 5430)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.api.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertEqual(app.config['PORT'], 80)
        self.assertEqual(app.config['MIN_FEE'], 1000)
        self.assertEqual(app.config['NETWORK'], 'mainnet')
        self.assertEqual(app.config['NETWORK'], 'https://testnet.blockchain.info')
        self.assertEqual(app.config['CONFIRMATIONS'], 6)
        self.assertEqual(app.config['MIN_CHANGE_VALUE'], 5430)


if __name__ == '__main__':
    unittest.main()
