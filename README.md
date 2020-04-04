# P2PKH Raw Transaction

This endpoint will be used to create a raw transaction that spends from a P2PKH address and that supports
paying to mulitple addresses (either P2PKH or P2SH). The endpoint should return a transaction that
spends from the source address and that pays to the output addresses. An extra output for change should
be included in the resulting transaction if the change is > 5430 SAT.


- *Path*: `/payment_transactions`
- *Method*: `POST`
- *Request Body*:
```
{
    source_address (string): The address to spend from
    outputs (dictionary): A dictionary that maps addresses to amounts (in SAT)
    fee_kb (int): The fee per kb in SAT
}
```

- *Response Body*:
```
{
    raw (string): The unsigned raw transaction
    inputs (array of dicts): The inputs used
    {
        txid (string): The transaction id
        vout (int): The output number
        script_pub_key (string): The script pub key
        amount (int): The amount in SAT
    }
}
```

- *Example*:
```shell script
curl -X POST \
  http://localhost:5000/payment_transactions \
  -H 'Content-Type: application/json' \ 
  -d '{
        "source_address": "3E1WB5Y7jxDPT428A3Si6g94L9j7Rt2vt4",
        "outputs": {
                "1HCuHELi5PX8mnLTSkPv27T48K4ig4CJUP": 9999
        },
        "fee_kb": 2500
}'
```

## Running

### Local

- Install packages and run:
```shell script
make start
```
OR 
```shell script
make install-packages
make run
```

## Docker

- Run:
```shell script
make docker
```
OR
```shell script
make docker-build
make docker-run
```

- Stop:
```shell script
make docker-stop
```

### Run unit tests

- Install test packages:
```shell script
make install-test-packages
```

- Run tests:
```shell script
make test
```

### Help

```shell script
make help
```
