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



## Running

### Local

- Install packages and run:
```shell
make start
```
OR 
```shell
make install-packages
make run
```

## Docker

- Run:
```shell
make docker
```
OR
```shell
make docker-build
make docker-run
```

- Stop:
```shell
make docker-stop
```

### Run unit tests

- Install test packages:
```shell
make install-test-packages
```

- Run tests:
```shell
make test
```

### Help

```shell
make help
```
