import getpass
import requests
from requests.exceptions import RequestException

# Centralized endpoint architecture configurations
BASE_URL = "http://127.0.0.1:5000"
REGISTER_ENDPOINT = f"{BASE_URL}/register"

def run_investigator_registration_client():
    """
    Captures user profile context safely and handles server proxy 
    network responses with strict connection error catchments.
    """
    print("=" * 60)
    print(" Pravah System: Investigator Identity Registration Client ")
    print("=" * 60)

    # 1. Capture payload items safely
    name = input("Enter investigator full name: ").strip()
    phone = input("Enter target contact phone number: ").strip()
    bike = input("Enter field asset vehicle/bike ID number: ").strip()
    
    # Securely hides keystrokes from terminal console view mirrors
    password = getpass.getpass("Enter secure profile account password: ")

    if not all([name, phone, bike, password]):
        print("\n❌ Client Input Validation Failure: All input fields are mandatory.")
        return

    payload = {
        "name": name,
        "phone": phone,
        "bike": bike,
        "password": password
    }

    print("\n⚡ Shipping identity context block to the blockchain gateway cluster...")

    # 2. Dispatch payload via network wire wrapped inside defensive catchments
    try:
        response = requests.post(
            REGISTER_ENDPOINT,
            json=payload,
            timeout=15  # Strict timeout prevents script from hanging forever if gateway stalls
        )

        print(f"👉 Gateway Server Communication Code: {response.status_code}")

        # 3. Handle data metrics payload safely depending on server return states
        try:
            response_data = response.json()
        except ValueError:
            # Fallback handling block if server outputs plain text or un-formatted HTML engine logs
            print(f"❌ Core Parsing Discrepancy: Received non-JSON error envelope body: {response.text}")
            return

        if response.status_code == 201:
            print("\n✅ PROFILE INITIALIZED SUCCESSFULLY ON LEDGER")
            print(f"  - Message:          {response_data.get('message')}")
            print(f"  - Transaction Hash: {response_data.get('transaction_hash')}")
            print(f"  - Block Number:     {response_data.get('block_number')}")
        else:
            # Displays human-readable message block returned from our Flask validations
            server_error_text = response_data.get("error", "An undocumented system exception occurred.")
            print(f"\n🛑 Registration Refused by Gateway Cluster: {server_error_text}")

    except RequestException as network_error:
        print(f"\n❌ Network Layer Exception: Unable to establish contact with the gateway server.")
        print(f"   Details: Verify that your Flask app is actively running on {BASE_URL}. Context: {network_error}")

    print("=" * 60)

if __name__ == "__main__":
    run_investigator_registration_client()
