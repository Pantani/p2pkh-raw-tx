from flask_restplus import Api
from flask import Blueprint

from .api.controller.payment import api as payment

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Create P2HKS Transactions',
    version='1.0',
    description='Create a raw transaction that spends from a P2PKH address.'
)
api.add_namespace(payment, path='/api')
