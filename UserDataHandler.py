from web3 import Web3, TestRPCProvider

class ContractHandler:
  def __init__(self):
    self.web3 = Web3(HTTPProvider(host='localhost', port='8545'))
    with open(str(path.join(dir_path, 'UserDataInterface.json')), 'r') as abi:
      self.abi = json.load(abi)
    self.contract_address = your_contract_address
    self.contract = self.web3.eth.contract(self.abi, self.contract_address)