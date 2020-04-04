import os


class Config:
    """
    Default configurations.
    """
    DEBUG = True
    PORT = os.getenv('PORT', 5000)
    MIN_FEE = os.getenv('MIN_FEE', 1000)
    NETWORK = os.getenv('NETWORK', 'testnet')
    API_URL = os.getenv('API_URL', 'https://blockchain.info')
    CONFIRMATIONS = os.getenv('CONFIRMATIONS', 0)
    MIN_CHANGE_VALUE = os.getenv('MIN_CHANGE_VALUE', 5430)


class DevelopmentConfig(Config):
    """
    Development configurations.
    """
    DEBUG = True
    PORT = os.getenv('PORT', 5000)
    MIN_FEE = os.getenv('MIN_FEE', 1000)
    NETWORK = os.getenv('NETWORK', 'mainnet')
    API_URL = os.getenv('API_URL', 'https://testnet.blockchain.info')
    CONFIRMATIONS = os.getenv('CONFIRMATIONS', 6)
    MIN_CHANGE_VALUE = os.getenv('MIN_CHANGE_VALUE', 5430)


class ProductionConfig(Config):
    """
    Production configurations.
    """
    DEBUG = False
    PORT = os.getenv('PORT', 5000)
    MIN_FEE = os.getenv('MIN_FEE', 1000)
    NETWORK = os.getenv('NETWORK', 'mainnet')
    API_URL = os.getenv('API_URL', 'https://blockchain.info')
    CONFIRMATIONS = os.getenv('CONFIRMATIONS', 6)
    MIN_CHANGE_VALUE = os.getenv('MIN_CHANGE_VALUE', 5430)
