import logging

from flask import request
from flask_restplus import Resource

from app.api.service.payment import Payment
from app.api.model.payment import PaymentRequest

log = logging.getLogger(__name__)

api = PaymentRequest.api
payment_body = PaymentRequest.body


@api.route('/payment_transactions')
class PaymentTransaction(Resource):
    """
    This resource creates a raw transaction that spends from a P2PKH address.
    """

    @api.doc('Creates a raw transaction from a P2PKH address')
    @api.expect(payment_body, validate=True)
    def post(self):
        try:
            post_data = request.json
            tx_obj = Payment.create_transaction(
                source_address=post_data["source_address"],
                outputs=post_data["outputs"],
                fee_kb=post_data["fee_kb"],
            )
            return tx_obj
        # TODO better error return
        except Exception as e:
            return e.to_dict()
