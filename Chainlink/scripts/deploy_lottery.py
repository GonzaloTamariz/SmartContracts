import time
import requests
from scripts.helful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    FORKED_LOCAL_ENVIROMENTS,
)
from brownie import Lottery, config, network


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
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
    # Fund lottery contract with link
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    # End lottery
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"{lottery.last_winner()} is the new winner")
    print(f"{lottery.random_number()}RANDOM")
    print(f"{lottery.random_index()}index contract")
    print(f"{lottery.random_number()%3} Index")


def main():
    lottery = deploy_lottery()
    input("Press Enter to continue...")
    print("Loteria 1")
    print("=========")
    start_lottery()
    buy_lotteryTicket()
    buy_lotteryTicket(id="Account2")
    buy_lotteryTicket(id="Account3")
    end_lottery()
