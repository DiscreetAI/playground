import asyncio
import time
import pprint
import requests

import rlp

from eth_utils import is_address
from ethereum.transactions import Transaction
from solc import compile_source, compile_files
from web3 import Web3, HTTPProvider
from web3.auto import w3
from web3.utils.events import get_event_data


def get_testnet_eth(to_address, provider=None):
	if provider:
		TEST_ACCOUNT = provider.eth.coinbase
		provider.eth.sendTransaction({"from": TEST_ACCOUNT, "to": to_address, "value": 9999999})
	else:
		to_whom = '{"toWhom":"%s"}' % to_address
		url = 'https://ropsten.faucet.b9lab.com/tap'
		requests.post(url, data=to_whom)

def send_raw_tx(w3, to_address, from_address, from_key):
	tx = Transaction(
		nonce=0,
		gasprice=w3.eth.gasPrice,
		startgas=100000,
		to=to_address,
		value=12345,
		data=b''
	)

	tx.sign(from_key)
	raw_tx = rlp.encode(tx)
	raw_tx_hex = w3.toHex(raw_tx)
	w3.eth.sendRawTransaction(raw_tx_hex)

def compile_source_file(file_path):
	with open(file_path, 'r') as f:
		source = f.read()

	return compile_source(source)




def deploy_Query(w3, contract_interface, account, target_accounts):
	tx_hash = w3.eth.contract(
		abi=contract_interface['abi'],
		bytecode=contract_interface['bin']).constructor(1, 1, target_accounts).transact({"from": account})

	address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
	return address

def deploy_Master(w3, contract_interface, account):
	tx_hash = w3.eth.contract(
		abi=contract_interface['abi'],
		bytecode=contract_interface['bin']).constructor().transact({"from": account})

	address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
	return address




def wait_for_receipt(w3, tx_hash, poll_interval):
	while True:
		tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
		if tx_receipt:
			return tx_receipt
		time.sleep(poll_interval)

def txn_digest(txn):
	return "Contract address: {0}\nEvent: {1}\nArg: {2}".format(
		txn['address'], txn['event'], txn['args'])

def event_callback(arg):
	print(txn_digest(arg))

def wait_on_tx_receipt(tx_hash):
	start_time = time.time()
	while True:
		if start_time + 60 < time.time():
			raise TimeoutError("Timeout occurred waiting for tx receipt")
		if w3.eth.getTransactionReceipt(tx_hash):
			return w3.eth.getTransactionReceipt(tx_hash)

def deploy_contract(w3, contract_interface):
	tx_hash = w3.eth.contract(
		abi=contract_interface['abi'],
		bytecode=contract_interface['bin']).constructor().transact({"from": acct})

	address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
	return address
