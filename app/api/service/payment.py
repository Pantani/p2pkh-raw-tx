import logging

from decimal import Decimal
from typing import Dict, List
from uncertainties import ufloat

from ..config import Config
from .unspent import Unspent as UnspentService
from ..exceptions.exceptions import EnoughFunds

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction
from bitcoin.wallet import CBitcoinAddress

log = logging.getLogger(__name__)


class Payment:

    @staticmethod
    def calculate_fee(input_count: int, output_count: int, fee_kb: int) -> int:
        """
        Calculates the transaction fee.
        (in*148 + out*34 + 10 plus or minus 'in')
            :param int input_count: number of inputs
            :param int output_count: number of outputs
            :param int fee_kb: the fee per kb in SAT
            :return: the fee value
        """
        size = ufloat(input_count * 148 + output_count * 34 + 10, input_count)
        fee = size * fee_kb
        if fee < Config.MIN_FEE:
            return Config.MIN_FEE

        return fee

    @staticmethod
    def select_unspent(unspent: List, value: int, output_count: int, fee_kb: int) -> (List, int):
        """
        Select unspent based in the amount.
            :param list unspent: a list of unspent utxos
            :param int value: the amount to be send
            :param int output_count: number of outputs
            :param int fee_kb: the fee per kb in SAT
            :return: an list of unspent objects and the transaction fee
        """
        # Try to find one utxo can satisfy the amount
        fee = Payment.calculate_fee(input_count=1, output_count=output_count, fee_kb=fee_kb)
        high = [u for u in unspent if u['value'] >= value + fee]
        high.sort(key=lambda u: u['value'])
        if len(high):
            return [high[0]], fee

        # Append the smalls utxo's to satisfy the amount
        low = [u for u in unspent if u['value'] < value]
        low.sort(key=lambda u: -u['value'])
        i, tv = 0, 0
        while tv < value + fee and i < len(low):
            fee = Payment.calculate_fee(input_count=i, output_count=output_count, fee_kb=fee_kb)
            tv += low[i]['value']
            i += 1
        if tv < value + fee:
            raise EnoughFunds(f'Not enough funds {tv} for value {value}')
        return low[:i], fee

    @staticmethod
    def create_transaction(source_address: str, outputs: Dict[str, Decimal], fee_kb: int) -> Dict:
        """
        Create the raw transaction with inputs.
            :param str source_address: the address to spend from
            :param dict outputs: a dictionary that maps addresses to amounts
            :param int fee_kb: the fee per kb in SAT
            :return: an dictionary of raw transaction
        """
        unspent = UnspentService.get_unspent_outputs(address=source_address, confirmations=Config.CONFIRMATIONS)
        unspent_amount = sum([u['value'] for u in unspent])

        total_amount = sum(outputs.values())
        inputs, fee = Payment.select_unspent(unspent=unspent, value=total_amount, output_count=len(outputs),
                                             fee_kb=fee_kb)

        change = total_amount - unspent_amount - fee
        if change > Config.MIN_CHANGE_VALUE:
            outputs[source_address] = change

        tx_obj = Payment.create_transaction_object(inputs=inputs, outputs=outputs)
        return {
            'raw': b2x(tx_obj.serialize()),
            'inputs': [{
                'txid': i['tx_hash'],
                'vout': i['tx_index'],
                'script_pub_key': i['script'],
                'amount': i['value'],
            } for i in inputs],
        }

    @staticmethod
    def create_transaction_object(inputs: List, outputs: Dict[str, Decimal]) -> CMutableTransaction:
        """
        Create the transaction object to calculate the raw transaction.
            :param list inputs: an array of unspent objects
            :param dict outputs: a dictionary that maps addresses to amounts
            :return: a transaction object
        """
        SelectParams(Config.NETWORK)

        tx_in: List[CMutableTxIn] = []
        for i in inputs:
            tx_id = lx(i["tx_hash"])
            vout = i["tx_index"]
            tx_in.append(CMutableTxIn(COutPoint(tx_id, vout)))

        tx_out: List[CMutableTxOut] = []
        for addr, amount in outputs.items():
            tx_out.append(CMutableTxOut(amount, CBitcoinAddress(addr).to_scriptPubKey()))

        return CMutableTransaction(tx_in, tx_out)
