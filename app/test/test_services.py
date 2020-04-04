import pytest

from typing import List
from decimal import Decimal

from bitcoin.wallet import CBitcoinAddress
from bitcoin.core import b2x, lx, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction

from app.api.service.payment import Payment as PaymentService
from app.api.exceptions.exceptions import EnoughFunds

from unittest import mock


@pytest.fixture
def source_address() -> str:
    return "1Po1oWkD2LmodfkBYiAktwh76vkF93LKnh"


@pytest.fixture
def valid_fee_kb() -> int:
    return 25000


@pytest.fixture
def unspent_1() -> List:
    return [{
        "tx_hash": "0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7",
        "tx_hash_big_endian": "e7343a4167bb1c2419364a5f7d8868f8731eafa243df2dcf97111099eaabb40b",
        "tx_index": 197306298,
        "tx_output_n": 3,
        "script": "76a9140180799618375ebd21bd67014deca9a167b8f91e88ac",
        "value": 1300,
        "value_hex": "00c65d40",
        "confirmations": 6
    }, {
        "tx_hash": "0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7",
        "tx_hash_big_endian": "e7343a4167bb1c2419364a5f7d8868f8731eafa243df2dcf97111099eaabb40b",
        "tx_index": 298994538,
        "tx_output_n": 3,
        "script": "76a9140180799618375ebd21bd67014deca9a167b8f91e88ac",
        "value": 13000000,
        "value_hex": "00c65d40",
        "confirmations": 6
    }]


@pytest.fixture
def unspent_2() -> List:
    return [
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 9,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 20273,
            "value_hex": "01914a",
            "confirmations": 1475,
            "tx_index": 0
        },
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 264,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 35273,
            "value_hex": "02549a",
            "confirmations": 1475,
            "tx_index": 0
        },
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 8,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 50073,
            "value_hex": "01914a",
            "confirmations": 1475,
            "tx_index": 0
        },
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 263,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 4703,
            "value_hex": "02549a",
            "confirmations": 1475,
            "tx_index": 0
        },
    ]


@pytest.fixture
def inputs_1() -> List:
    return [
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 9,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 20273,
            "value_hex": "01914a",
            "confirmations": 1475,
            "tx_index": 0
        },
    ]


@pytest.fixture
def inputs_2() -> List:
    return [
        {
            "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 9,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 20273,
            "value_hex": "01914a",
            "confirmations": 1475,
            "tx_index": 0
        },
        {
            "tx_hash": "0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7",
            "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
            "tx_output_n": 264,
            "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
            "value": 35273,
            "value_hex": "02549a",
            "confirmations": 1475,
            "tx_index": 0
        }
    ]


@pytest.fixture
def outputs_1() -> dict:
    return dict(mvDvYba71W8at5sU9G8ELqQph8s7fKgbiA=Decimal(100000))


@pytest.fixture
def outputs_2() -> dict:
    return dict(
        mhnnkpnCfBkxN5KpfMArye2F376nATVJDW=100000,
        mvDvYba71W8at5sU9G8ELqQph8s7fKgbiA=2000,
        msrXsFAeRMLnY9mGPyeVwZZqxqVQUXh4uh=20000000,
    )


@pytest.mark.parametrize("input_count,output_count,fee_kb,expected", [
    (1, 10, 25000, 12450),
    (3, 1, 25000, 12200),
    (40, 200, 25000, 318250),
    (1, 2, -1, 1000),
    (10, 10, 10, 1000),
])
def test_calculate_fee(input_count: int, output_count: int, fee_kb: int, expected: int):
    result = PaymentService.calculate_fee(input_count=input_count, output_count=output_count, fee_kb=fee_kb)
    assert result == expected


@pytest.mark.parametrize("value,output_count", [
    (13000000, 0),
    (13000000, 1),
    (130000000, 2),
    (12900000, 1000),
])
def test_select_unspent_enough_funds(value: int, output_count: int, valid_fee_kb, unspent_1):
    with pytest.raises(EnoughFunds):
        PaymentService.select_unspent(unspent=unspent_1, value=value, output_count=output_count, fee_kb=valid_fee_kb)


@pytest.mark.parametrize("value,output_count,expected_fee", [
    (8000000, 0, 3950),
    (120, 10, 12450),
    (1300000, 4, 7350),
])
def test_select_unspent_1(value: int, output_count: int, expected_fee: int, valid_fee_kb, unspent_1):
    r = PaymentService.select_unspent(unspent=unspent_1, value=value, output_count=output_count, fee_kb=valid_fee_kb)
    assert r == ([unspent_1[1]], expected_fee)


@pytest.mark.parametrize("value,output_count,expected_fee", [
    (69445, 20, 28350),
    (78381, 4, 14750),
])
def test_select_unspent_2(value: int, output_count: int, expected_fee: int, valid_fee_kb, unspent_2):
    r = PaymentService.select_unspent(unspent=unspent_2, value=value, output_count=output_count, fee_kb=valid_fee_kb)
    assert r == ([unspent_2[2], unspent_2[1], unspent_2[0]], expected_fee)


def test_create_transaction_object_1(inputs_1, outputs_1):
    r = PaymentService.create_transaction_object(inputs=inputs_1, outputs=outputs_1)

    tx_in: List[CMutableTxIn] = [
        CMutableTxIn(COutPoint(lx('4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b'), 0))]

    pk = CBitcoinAddress('mvDvYba71W8at5sU9G8ELqQph8s7fKgbiA').to_scriptPubKey()
    tx_out: List[CMutableTxOut] = [CMutableTxOut(100000, pk)]

    expected = CMutableTransaction(tx_in, tx_out)
    assert b2x(r.serialize()) == b2x(expected.serialize())


def test_create_transaction_object_2(inputs_2, outputs_2):
    r = PaymentService.create_transaction_object(inputs=inputs_2, outputs=outputs_2)

    tx_in: List[CMutableTxIn] = [
        CMutableTxIn(COutPoint(lx('4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b'), 0)),
        CMutableTxIn(COutPoint(lx('0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7'), 0)),
    ]

    pk1 = CBitcoinAddress('mhnnkpnCfBkxN5KpfMArye2F376nATVJDW').to_scriptPubKey()
    pk2 = CBitcoinAddress('mvDvYba71W8at5sU9G8ELqQph8s7fKgbiA').to_scriptPubKey()
    pk3 = CBitcoinAddress('msrXsFAeRMLnY9mGPyeVwZZqxqVQUXh4uh').to_scriptPubKey()
    tx_out: List[CMutableTxOut] = [
        CMutableTxOut(100000, pk1),
        CMutableTxOut(2000, pk2),
        CMutableTxOut(20000000, pk3),
    ]

    expected = CMutableTransaction(tx_in, tx_out)
    assert b2x(r.serialize()) == b2x(expected.serialize())


@mock.patch('requests.get')
def test_create_transaction(mock_get, source_address, outputs_2, valid_fee_kb):
    mock_get.return_value.status_code = 200
    mock_get.return_value = mock.Mock(ok=True)
    mock_get.return_value.json.return_value = {
        "unspent_outputs": [
            {
                "tx_hash": "0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7",
                "tx_hash_big_endian": "e7343a4167bb1c2419364a5f7d8868f8731eafa243df2dcf97111099eaabb40b",
                "tx_output_n": 3,
                "script": "76a9140180799618375ebd21bd67014deca9a167b8f91e88ac",
                "value": 15002730,
                "value_hex": "00c65d40",
                "confirmations": 6,
                "tx_index": 298994538
            },
            {
                "tx_hash": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
                "tx_hash_big_endian": "5b918d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde6985412145",
                "tx_output_n": 20,
                "script": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
                "value": 10299730,
                "value_hex": "01914a",
                "confirmations": 1475,
                "tx_index": 0
            },
        ]
    }

    r = PaymentService.create_transaction(source_address=source_address, outputs=outputs_2, fee_kb=valid_fee_kb)
    assert r == {
        "raw": "0100000002e7343a4167bb1c2419364a5f7d8868f8731eafa243df2dcf97111099eaabb40b6a4bd21100ffffffff5b91"
               "8d9adcdcd48877a6534c31958cc4c97a5635c5d3d2d5782fde69854121450000000000ffffffff03a086010000000000"
               "1976a91418eef1d5d14e8032ca7caacefce7164179320b9388acd0070000000000001976a914a1515aee272e49cd1e2f9"
               "c3490743c4b232d265088ac002d3101000000001976a91487556ff8cc729dd743ee7bf33302098135b95c5e88ac00000000",
        "inputs": [
            {
                "txid": "0bb4abea99101197cf2ddf43a2af1e73f868887d5f4a3619241cbb67413a34e7",
                "vout": 298994538,
                "script_pub_key": "76a9140180799618375ebd21bd67014deca9a167b8f91e88ac",
                "amount": 15002730
            },
            {
                "txid": "4521418569de2f78d5d2d3c535567ac9c48c95314c53a67788d4dcdc9a8d915b",
                "vout": 0,
                "script_pub_key": "76a914fa0692278afe508514b5ffee8fe5e97732ce066988ac",
                "amount": 10299730
            }
        ]
    }
