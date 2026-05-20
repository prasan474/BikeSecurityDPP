from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Connection Failed")

# Deployed Contract Address
contract_address = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"

# Updated ABI from BikeSecurity.json
contract_abi = [
{
"anonymous": False,
"inputs":[
{"indexed":False,"internalType":"string","name":"phone","type":"string"},
{"indexed":False,"internalType":"string","name":"location","type":"string"},
{"indexed":False,"internalType":"uint256","name":"timestamp","type":"uint256"}
],
"name":"SensorTriggered",
"type":"event"
},
{
"anonymous":False,
"inputs":[{"indexed":False,"internalType":"string","name":"phone","type":"string"}],
"name":"UserLoggedIn",
"type":"event"
},
{
"anonymous":False,
"inputs":[{"indexed":False,"internalType":"string","name":"phone","type":"string"}],
"name":"UserRegistered",
"type":"event"
},
{
"inputs":[{"internalType":"string","name":"phone","type":"string"}],
"name":"registerUser",
"outputs":[],
"stateMutability":"nonpayable",
"type":"function"
},
{
"inputs":[{"internalType":"string","name":"phone","type":"string"}],
"name":"loginUser",
"outputs":[],
"stateMutability":"nonpayable",
"type":"function"
},
{
"inputs":[
{"internalType":"string","name":"phone","type":"string"},
{"internalType":"string","name":"location","type":"string"}
],
"name":"triggerSensor",
"outputs":[],
"stateMutability":"nonpayable",
"type":"function"
},
{
"inputs":[{"internalType":"string","name":"phone","type":"string"}],
"name":"getAlertHistory",
"outputs":[
{"components":[
{"internalType":"string","name":"phone","type":"string"},
{"internalType":"string","name":"location","type":"string"},
{"internalType":"uint256","name":"timestamp","type":"uint256"}
],
"internalType":"struct BikeSecurity.SensorAlert[]",
"name":"",
"type":"tuple[]"
}
],
"stateMutability":"view",
"type":"function"
}
]

# Create Contract Object
contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# Use first Ganache account
account = web3.eth.accounts[0]

# Temporary storage for user details
users = {}


# REGISTER API
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    phone = data["phone"]
    bike = data["bike"]
    password = data["password"]

    users[phone] = {
        "name": name,
        "bike": bike,
        "password": password
    }

    # Blockchain Transaction
    tx = contract.functions.registerUser(phone).transact({
        "from": account
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx)

    return jsonify({
        "message": "User Registered Successfully",
        "transaction_hash": tx.hex(),
        "block_number": receipt.blockNumber
    })


# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    phone = data["phone"]
    password = data["password"]

    if phone in users and users[phone]["password"] == password:

        tx = contract.functions.loginUser(phone).transact({
            "from": account
        })

        receipt = web3.eth.wait_for_transaction_receipt(tx)

        return jsonify({
            "message": "Login Successful",
            "transaction_hash": tx.hex(),
            "block_number": receipt.blockNumber
        })

    return jsonify({"message": "Invalid Credentials"})


# SENSOR TRIGGER API
@app.route("/trigger", methods=["POST"])
def trigger():

    data = request.json
    phone = data["phone"]
    location = data.get("location", "Unknown")

    tx = contract.functions.triggerSensor(phone, location).transact({
        "from": account
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx)

    return jsonify({
        "message": "Sensor Triggered",
        "transaction_hash": tx.hex(),
        "block_number": receipt.blockNumber
    })


# ALERT HISTORY API
@app.route("/history", methods=["GET"])
def history():

    phone = request.args.get("phone")

    alerts = contract.functions.getAlertHistory(phone).call()

    result = [
        {
            "phone": a[0],
            "location": a[1],
            "timestamp": a[2]
        }
        for a in alerts
    ]

    return jsonify(result)


# HOME ROUTE
@app.route("/")
def home():
    return "Bike Security Blockchain Backend Running"


if __name__ == "__main__":
    app.run(debug=True)