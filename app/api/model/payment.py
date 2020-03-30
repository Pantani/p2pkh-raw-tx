from flask_restplus import Namespace, fields


class PaymentRequest:
    """
    Payment request model.
    """
    api = Namespace('payment', description='payment related operations')
    body = api.model('payment', {
        'source_address': fields.String(required=True, description='source address'),
        'outputs': fields.Raw(required=True, description='outputs to send transaction'),
        'fee_kb': fields.Integer(required=True, description='the fee value in kb\'s'),
    })
