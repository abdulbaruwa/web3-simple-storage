// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // default value for an unit gets inititalised to 0
    uint256 favouriteNumber;
    bool favouriteBool;

    struct People {
        uint256 favouriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function store(uint256 _favouriteNumber) public returns (uint256) {
        favouriteNumber = _favouriteNumber;
        return favouriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favouriteNumber;
    }

    // memory string value is deleted after call is complete. A storage key word can preseed a string, this is used in cases where the string value will persist even after the function has been executed.
    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber, _name));
        nameToFavouriteNumber[_name] = _favouriteNumber;
    }

    function calc(uint256 number) public pure returns (uint256) {
        return number * number;
    }
}
