from flask_restx import Namespace, fields


class PaymentRequest:
    """
    Payment request model.
    """
    api = Namespace('payment', description='payment related operations')
    body = api.model('payment', {
        'source_address': fields.String(required=True, min_length=25, max_length=36, description='source address'),
        'outputs': fields.Raw(required=True, description='outputs to send transaction'),
        'fee_kb': fields.Integer(required=True, unsigned=True, description='the fee value in kb\'s'),
    })
