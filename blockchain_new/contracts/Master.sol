pragma solidity 0.4.19;

import "./Query.sol";


contract Master {
    using strings for *;

    address public owner;
    uint256 public id;
    mapping(address => uint256[]) public queries;
    mapping(uint256 => address) private addressBook;

    event QueryCreated(uint256 id);

    modifier queryOwner(uint256 id) {
        require(ownershipChecker(id, msg.sender));
        _;
    }

    function Master() public {
        owner = msg.sender;
    }

    function () public payable {
        revert();
    }

    function query(address originator, string[] searchFields)
        public
        payable
    {
        address[] outreach = apiCall(searchFields);       // needs to be implemented
        Query query = new Query(originator, msg.value, searchFields, id, outreach);
        emit QueryCreated(id);
        queries[originator].push(id);
        addressBook[id] = query.address;
        id++;
    }

    function requestRefund(uint256 _id) public queryOwner(_id) {
        Query query = Query(idToAddress(_id));
        query.cancel();
        query.originator.transfer(query.bounty);
        emit Cancel(_id);
    }

    function idToAddress(uint256 _id) private view queryOwner(_id) {
        return addressBook[_id];
    }

    function ownershipChecker(uint256 _id, address proposer)
        private
        view
        returns (bool)
    {
        uint256 lst = queries[proposer];
        for (int i = 0; i < lst.length; i++) {
            if (lst[i] == _id) {
                return true;
            }
        }
        return false;
    }
}