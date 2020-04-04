import logging

from flask import request
from flask_restx import Resource

from app.api.service.payment import Payment
from app.api.model.payment import PaymentRequest
from app.api.exceptions.exceptions import ApiException

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
        except ApiException as e:
            return e.to_dict()
        except Exception as e:
            return ApiException(str(e)).to_dict()
