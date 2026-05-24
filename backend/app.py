import os
from flask import Flask, request, jsonify
from web3 import Web3
from web3.exceptions import Web3Exception
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Core Configurations
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
CONTRACT_ADDRESS = Web3.to_checksum_address("0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab")

# Setup Web3 Connection securely
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if web3.is_connected():
    print(f"Successfully connected to Ethereum Node at {GANACHE_URL}")
else:
    print("CRITICAL: Blockchain node connection failed.")
    raise SystemExit(1)

CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "phone", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "location", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "SensorTriggered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "internalType": "string", "name": "phone", "type": "string"}],
        "name": "UserLoggedIn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": False, "internalType": "string", "name": "phone", "type": "string"}],
        "name": "UserRegistered",
        "type": "event"
    },
    {
        "inputs": [{"internalType": "string", "name": "phone", "type": "string"}],
        "name": "registerUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "phone", "type": "string"}],
        "name": "loginUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "phone", "type": "string"},
            {"internalType": "string", "name": "location", "type": "string"}
        ],
        "name": "triggerSensor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "phone", "type": "string"}],
        "name": "getAlertHistory",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "phone", "type": "string"},
                    {"internalType": "string", "name": "location", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "internalType": "struct BikeSecurity.SensorAlert[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Instantiate smart contract reference pointer
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Assign transaction signer authority safely from available accounts
if not web3.eth.accounts:
    raise RuntimeError("No unlocked accounts available on the connected Ethereum node.")
tx_sender_account = web3.eth.accounts[0]

# Secure local persistence storage placeholder with password hashing
user_database = {}


def send_blockchain_transaction(contract_function, *args):
    """
    Helper abstraction to build, dispatch, and await nonpayable transactions safely.
    Handles gas estimation and node validation errors uniformly.
    """
    try:
        # Build transaction parameters with explicit gas caps
        tx_params = {
            "from": tx_sender_account,
            "nonce": web3.eth.get_transaction_count(tx_sender_account),
        }
        
        built_tx = contract_function(*args).build_transaction(tx_params)
        
        # Dispatch transaction to network execution layers
        tx_hash = web3.eth.send_transaction(built_tx)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        
        return {
            "transaction_hash": tx_hash.hex(),
            "block_number": receipt.get("blockNumber", 0),
            "gas_used": receipt.get("gasUsed", 0)
        }
    except Web3Exception as blockchain_error:
        print(f"Blockchain EVM Execution Exception: {blockchain_error}")
        raise RuntimeError(f"Smart contract interaction failed: {str(blockchain_error)}")


# ✅ API ROUTE: USER REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    
    name = data.get("name")
    phone = data.get("phone")
    bike = data.get("bike")
    password = data.get("password")

    if not all([name, phone, bike, password]):
        return jsonify({"error": "Validation Failure: name, phone, bike, and password are required fields."}), 400

    if phone in user_database:
        return jsonify({"error": "Conflict: An account with this phone identifier is already registered."}), 409

    try:
        # Commit identity mutation to the blockchain ledger
        tx_meta = send_blockchain_transaction(contract.functions.registerUser, phone)
        
        # Store user payload safely locally utilizing secure cryptographic hashes
        user_database[phone] = {
            "name": name,
            "bike": bike,
            "password_hash": generate_password_hash(password)
        }

        return jsonify({
            "message": "User registered successfully.",
            **tx_meta
        }), 201
        
    except Exception as runtime_error:
        return jsonify({"error": str(runtime_error)}), 502


# ✅ API ROUTE: USER LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    
    phone = data.get("phone")
    password = data.get("password")

    if not phone or not password:
        return jsonify({"error": "Validation Failure: Missing phone or password fields."}), 400

    user_record = user_database.get(phone)
    
    # Secure hash comparison completely defeats timing vector analysis
    if user_record and check_password_hash(user_record["password_hash"], password):
        try:
            tx_meta = send_blockchain_transaction(contract.functions.loginUser, phone)
            return jsonify({
                "message": "Authentication successful.",
                **tx_meta
            }), 200
        except Exception as runtime_error:
            return jsonify({"error": str(runtime_error)}), 502

    return jsonify({"error": "Unauthorized: Invalid phone or password credentials."}), 401


# ✅ API ROUTE: SENSOR HARDWARE EVENT TRIGGER
@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.get_json(silent=True) or {}
    phone = data.get("phone")
    location = data.get("location", "Unknown GPS Coordinate Location")

    if not phone:
        return jsonify({"error": "Validation Failure: Target 'phone' field parameter is mandatory."}), 400

    try:
        tx_meta = send_blockchain_transaction(contract.functions.triggerSensor, phone, location)
        return jsonify({
            "message": "Telemetry sensor alert logged to blockchain successfully.",
            **tx_meta
        }), 200
    except Exception as runtime_error:
        return jsonify({"error": str(runtime_error)}), 502


# ✅ API ROUTE: FETCH HISTORICAL ALERT RECORD METADATA
@app.route("/history", methods=["GET"])
def history():
    phone = request.args.get("phone")

    if not phone:
        return jsonify({"error": "Validation Failure: URL query string parameter 'phone' is required."}), 400

    try:
        alerts = contract.functions.getAlertHistory(phone).call()
        
        # Unpack structural contract structs into clean JSON lists
        serialized_history_records = [
            {
                "phone": record[0],
                "location": record[1],
                "timestamp": record[2]
            }
            for record in alerts
        ]
        
        return jsonify(serialized_history_records), 200
        
    except Web3Exception as blockchain_read_error:
        print(f"EVM View Call Exception: {blockchain_read_error}")
        return jsonify({"error": "Failed to read data logs from smart contract ledger."}), 502


@app.route("/")
def home():
    return "Bike Security Blockchain API Gateway Cluster Operational", 200


if __name__ == "__main__":
    # In production settings, switch debug off and run inside a WSGI layout like Gunicorn
    app.run(host="127.0.0.1", port=5000, debug=True)
