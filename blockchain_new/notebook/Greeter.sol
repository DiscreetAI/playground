pragma solidity 0.4.20;

contract Greeter{
	
	string private greeting;

	function Greeter() public {
		greeting = "hello, World!";
	}

	function greet() public view returns(string) {
		return greeting;
	}

}
