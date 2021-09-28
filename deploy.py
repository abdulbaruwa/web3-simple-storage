from solcx import compile_standard, install_solc
import json

from web3 import Web3
import web3 
import os
from dotenv import load_dotenv

# looks and import .env file and import it into the script
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

install_solc("0.6.0")

# compile the solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# dump compiled sol in json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# deploy
# get the bytecode from the compiled output
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# print(bytecode)

# get the ABI, from the compiled sol
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print(abi)

# connect to test local blockchain
w3 =  Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = os.getenv("MY_ADDRESS")
print(my_address)

# Remember to prefic private key from Genache with "0x"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# build our transaction
# sign the transaction
# send a transaction

# nounce : from latest transaction count
nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from":my_address, "nonce": nonce})

# print(transaction)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)

# send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("signed transaction sent")


# Working with contracts, we will need:
# The contract ABI
# Contract Address

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# When making transactions to the blockchain. There are two ways we can interact with them
# by Call -> Simulates making the call and getting a return value. Those not effect a state change on the block
# by Transact -> Makes a state change on the block chain

print(simple_storage.functions.retrieve().call())

# note nonce can only be used once
store_transaction = simple_storage.functions.store(15).buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce + 1})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())