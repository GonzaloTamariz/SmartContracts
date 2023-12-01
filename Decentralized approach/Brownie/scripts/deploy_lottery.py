import time
import requests
from scripts.helful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    FORKED_LOCAL_ENVIROMENTS,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)

from brownie import Lottery, config, network, Oracle


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery contract")
    return lottery


def deploy_oracle():
    account = get_account()
    oracle = Oracle.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed oracle contract")
    return oracle


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started")


def buy_lotteryTicket(id=None, index=None):
    account = get_account(id=id, index=index)
    lottery = Lottery[-1]
    value = lottery.getTicketPrice() + 100000000
    tx = lottery.buyTicket({"from": account, "value": value})
    tx.wait(1)
    print("You entered de lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    # write_random_number(index=2, value=12)
    time.sleep(5)
    print(f"{lottery.last_winner()} is the new winner")
    print(f"{lottery.random_number()}RANDOM")
    print(f"{lottery.random_index()}index contract")
    print(f"{lottery.random_number()%6} Index")


def write_random_number(id=None, index=None, value=3):
    account = get_account(id=id, index=index)
    lottery = Lottery[-1]
    tx = lottery.updateRequest(0, value, {"from": account})
    tx.wait(1)
    print("ACCOUNT:" + str(get_account(index=2)))
    print("MALICIOUS NUMBER: " + str(value))


def main():
    lottery = deploy_lottery()
    url = ""
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        print("LOCAL GANACHE")
        url = "http://localhost:8080/api/addressganache"
    else:
        print("TESTNET RINKEBY")
        url = "http://localhost:8080/api/addressrinkeby"

    response = requests.post(url, data=str(Lottery[-1]))

    input("Press Enter to continue...")

    print("Loteria 1")
    print("=========")
    start_lottery()
    buy_lotteryTicket(index=0)
    buy_lotteryTicket(index=1)
    buy_lotteryTicket(index=2)
    buy_lotteryTicket(index=3)
    buy_lotteryTicket(index=4)
    buy_lotteryTicket(index=5)
    end_lottery()
    input("Press Enter to continue...")
    print("Loteria 2")
    print("=========")
    start_lottery()
    buy_lotteryTicket(index=0)
    buy_lotteryTicket(index=1)
    buy_lotteryTicket(index=2)
    buy_lotteryTicket(index=3)
    buy_lotteryTicket(index=4)
    buy_lotteryTicket(index=5)
    end_lottery()
    input("Press Enter to continue...")
    print("Loteria 3")
    print("=========")
    start_lottery()
    buy_lotteryTicket(index=0)
    buy_lotteryTicket(index=1)
    buy_lotteryTicket(index=2)
    buy_lotteryTicket(index=3)
    buy_lotteryTicket(index=4)
    buy_lotteryTicket(index=5)
    end_lottery()
