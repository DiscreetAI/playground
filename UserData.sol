  #smart contract functionality: transfer
  #smart contract structs: mapping of datasets to amounts paid (basically an augmented transaction history)
  #smart contract exchanges data | seller -> buyer and token | buyer -> seller
  #price minimum
  
  #mobile app functionality: show user transaction history and smart contract balance
  	#provide transaction history by parsing through events of smart contract
    #allow user to input new data for sale
  
  #server needs to get information from smart contract and provides it to mobile
  	#>means that server needs to have a data structure of smart contract addresses
    #POST(<smart contract address>) returns TRNXN HISTORY // add endpoint to server
    
//https://docs.bigchaindb.com/en/latest/permissions.html#read-permissions
//https://ethereum.stackexchange.com/questions/2024/how-to-access-the-event-log-by-knowing-the-contract-address-web3
//pro tip: use remix to get web3 deployment code (straight up copy code into remix, then get the web3 deployment code)
/////////////////////////////////////////////////
  
pragma solidity ^0.4.15;

contract UserData {

address serverAddress;
address userAddress;

mapping (string => bytes32) datasets;
mapping (string => uint256) datasetBalances;

mapping (address => uint256) balances;

modifier isServer() {
require(msg.sender == serverAddress);
_;
}

event Transfer(
address _requester,
uint256 _value,
string _dataset
);
event Withdrawal(address user, uint amount);

function UserData(address _userAddress) public {

serverAddress = msg.sender;
userAddress = _userAddress;

}

function addDataSet(string dataset, bytes32 ipfsPointer)
public returns(bool) {

datasets[dataset] = ipfsPointer;
}


function transfer(string dataset) payable public returns (bytes32 pointer) {

if (datasetBalances[dataset] + msg.value < datasetBalances[dataset] || balances[userAddress] + msg.value < balances[userAddress]) {
revert();
}

datasetBalances[dataset] += msg.value;
balances[userAddress] += msg.value;

//rekey encrypted data on ipfs

Transfer(msg.sender, msg.value, dataset);

return datasets[dataset];
}

function withdraw()
public returns (uint transferedAmount) {
if (balances[msg.sender] == 0) {
return 0;
}

uint transferAmount = balances[msg.sender];
balances[msg.sender] = 0;
msg.sender.transfer(transferAmount);
Withdrawal(msg.sender, transferAmount);
return transferAmount;
}

/* Fallback function */
function() payable public {
revert();
}

}