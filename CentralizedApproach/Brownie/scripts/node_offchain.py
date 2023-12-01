import sys
import json
import requests
from web3 import Web3
import asyncio
from brownie import Lottery, Oracle, network, config, Contract
from scripts.helful_scripts import (
    get_account,
    FORKED_LOCAL_ENVIROMENTS,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)

# Connection information
url = ""
if (
    network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
    or network.show_active() in FORKED_LOCAL_ENVIROMENTS
):
    print("LOCAL GANACHE")
    url = "http://localhost:8545"
    url_address = "http://localhost:8080/api/addressganache"
else:
    print("TESTNET RINKEBY")
    url = "https://rinkeby.infura.io/v3/85255d60dc214513a8eef637d7c284ce"
    url_address = "http://localhost:8080/api/addressrinkeby"


web3 = Web3(Web3.HTTPProvider(url))
# Contract address and abi
response = requests.get(url_address)
data = response.text
parse_json = json.loads(data)
contract_address = parse_json["address"]
contract_abi = Lottery.abi
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
print("Contract address: " + contract_address)

# ID of the node: Account who manage the node.
account = ""
secret_key = ""
if (
    network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
    or network.show_active() in FORKED_LOCAL_ENVIROMENTS
):
    # Local-Ganache
    account = "0xB5fB12fd8148441fE7Ad208135dC376923Ff349B"
    secret_key = "0x2F45E72EAEDFB7F2F9AFA52C1B80D7E69C2BAC1CFD35EE746D2AED93917F397B"
else:
    # Testnet-Rinkeby
    account = "0xbB8147F66FaF71A5bA41E5bD074d6562bd9DB362"
    secret_key = config["wallets"]["from_key"]
print("Account: ", account)


def handle_event(event):
    # First we extract id and url of the event
    event_json = Web3.toJSON(event)
    id = event["args"]["id"]
    url = event["args"]["url"]
    print("ID:", id)
    # Now, we send a get to URL
    response_API = requests.get("http://localhost:8080/api/random")
    # We extract data from responese
    data = response_API.text
    parse_json = json.loads(data)
    # We get the random_number
    random_number = parse_json["value"]
    print("Random number", random_number)
    # Store random_number in the smart contract
    raw_transaction = contract.functions.updateRequest(
        id, random_number
    ).buildTransaction(
        {
            "gas": 6721975,
            "from": account,
            "nonce": web3.eth.getTransactionCount(account),
        }
    )

    signed = web3.eth.account.signTransaction(
        raw_transaction,
        secret_key,
    )
    receipt = web3.eth.sendRawTransaction(signed.rawTransaction)
    web3.eth.waitForTransactionReceipt(receipt)

    print("Random number stored in the blockchain")


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "NewRequest" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for NewRequest in event_filter.get_new_entries():
            handle_event(NewRequest)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "NewRequest" event for Lottery contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.NewRequest.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()
