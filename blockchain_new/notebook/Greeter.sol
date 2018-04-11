pragma solidity 0.4.20;

contract Greeter {
	string private greeting;

	emit event Greeting(address person);

	function Greeter() public {
		Greeting(msg.sender);
		greeting = "hello, World!";
	}

	function greet() public view returns(string) {
		return greeting;
	}

}
