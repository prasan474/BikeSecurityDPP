// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BikeSecurity {

    // EVENTS

    event UserRegistered(string phone);
    event UserLoggedIn(string phone);
    event SensorTriggered(string phone, string location, uint256 timestamp);


    // USER STRUCTURE

    struct User {
        string phone;
        bool registered;
    }


    // ALERT STRUCTURE

    struct SensorAlert {
        string phone;
        string location;
        uint256 timestamp;
    }


    // USER STORAGE

    mapping(string => User) public users;


    // ALERT HISTORY STORAGE

    mapping(string => SensorAlert[]) private alertHistory;


    // REGISTER USER

    function registerUser(string memory phone) public {

        require(!users[phone].registered, "User already registered");

        users[phone] = User(phone, true);

        emit UserRegistered(phone);
    }


    // LOGIN USER

    function loginUser(string memory phone) public {

        require(users[phone].registered, "User not registered");

        emit UserLoggedIn(phone);
    }


    // SENSOR TRIGGER FUNCTION

    function triggerSensor(string memory phone, string memory location) public {

        require(users[phone].registered, "User not registered");

        alertHistory[phone].push(SensorAlert(phone, location, block.timestamp));

        emit SensorTriggered(phone, location, block.timestamp);
    }


    // GET ALERT HISTORY

    function getAlertHistory(string memory phone) public view returns (SensorAlert[] memory) {

        return alertHistory[phone];
    }

}