from random import random
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    get_account,
    get_contract,
)


def test_get_TicketPrice():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act
    # 2000 eth /usd
    # usdEntryFee is 50
    # 2000/1 == 50/x == 0.025
    expected_ticket_price = Web3.toWei(5 / 2000, "ether")
    ticket_price = lottery.getTicketPrice()

    # Assert

    assert expected_ticket_price == ticket_price


def test_cant_buyTicket_unless_started():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    # ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.buyTicket({"from": get_account(), "value": lottery.getTicketPrice()})


def test_can_start_and_buyTicket():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # ACT
    lottery.buyTicket({"from": account, "value": lottery.getTicketPrice()})
    # Assert
    assert lottery.lottery_players(0) == account


def test_can_end_lottery():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.buyTicket({"from": account, "value": lottery.getTicketPrice()})
    # ACT
    lottery.endLottery({"from": account})
    # ASSERT
    assert lottery.state() == 1


def test_can_pick_winner_correctly():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.buyTicket({"from": account, "value": lottery.getTicketPrice()})
    lottery.buyTicket({"from": get_account(index=1), "value": lottery.getTicketPrice()})
    lottery.buyTicket({"from": get_account(index=2), "value": lottery.getTicketPrice()})
    # ACT
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    transaction = lottery.endLottery({"from": account})
    expected_winner_index = lottery.random_number() % 3
    # ASSERT
    assert lottery.last_winner() == get_account(expected_winner_index)
    assert lottery.balance() == 0
    # assert account.balance() == starting_balance_of_account + balance_of_lottery
