from web3 import Web3, HTTPProvider

class ContractHandler:
  def __init__(self):
    self.web3 = Web3(HTTPProvider(host='localhost', port='8545'))
    with open(str(path.join(dir_path, 
    	'UserDataInterface.json')), 
    	'r') as abi:
      self.abi = json.load(abi)
    self.contract_address = '0x8283e96f9eec01c301d3308e470ef2e43d858e24'
    self.contract = self.web3.eth.contract(self.abi, self.contract_address)
    # self.web3.personal.unlockAccount(
    # 	'8b7343647f237415bcf0d3f06ea82e028fe043a2', 
    # 	ethaccountpassword)
    transaction = {'from': self.web3.eth.accounts[0], 'gas': 410000}
    self.hash = self.contract.deploy(transaction)
    self.receipt = self.web3.eth.getTransactionReceipt(self.hash)
    self.contract_address = self.receipt['contractAddress']