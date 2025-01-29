import os
import time
import requests
import random
from itertools import cycle
from mnemonic import Mnemonic
from eth_account import Account
from fake_useragent import UserAgent

# ==============================================
# CONFIGURATION (UPDATE THESE VALUES)
# ==============================================
REFERRAL_CODE = "YOUR_REFERRAL_CODE_HERE"
PROXIES_FILE = "proxies.txt"
API_SIGNUP_URL = "https://testnet.humanity.org/api/signup"
WALLETS_DIR = "wallets"
REQUEST_DELAY = 5  # Longer delay to avoid rate limits

# ==============================================
# WALLET GENERATION (NO RUST DEPENDENCIES)
# ==============================================
def generate_wallet():
    """Generate Ethereum wallet using pure Python libraries"""
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    
    # Derive private key and address from mnemonic
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(mnemonic)
    
    return mnemonic, account.address, account.key.hex()

def save_wallet(mnemonic, address, private_key):
    os.makedirs(WALLETS_DIR, exist_ok=True)
    with open(os.path.join(WALLETS_DIR, f"{address}.txt"), "w") as f:
        f.write(f"Mnemonic: {mnemonic}\nAddress: {address}\nPrivate Key: {private_key}\n")

# ==============================================
# PROXY AND ACCOUNT CREATION
# ==============================================
def load_proxies():
    with open(PROXIES_FILE, "r") as f:
        return cycle([line.strip() for line in f if line.strip()])

proxies_pool = load_proxies()
user_agent = UserAgent()

def generate_email():
    return f"user{random.randint(10**9, 10**10)}@tmpmail.org"

def create_account(proxy):
    try:
        headers = {"User-Agent": user_agent.random}
        proxy_config = {"http": proxy, "https": proxy}
        
        mnemonic, address, private_key = generate_wallet()
        
        payload = {
            "email": generate_email(),
            "password": "SecurePass123!",
            "referral_code": REFERRAL_CODE,
            "wallet_address": address
        }
        
        response = requests.post(
            API_SIGNUP_URL,
            json=payload,
            headers=headers,
            proxies=proxy_config,
            timeout=20
        )
        
        if response.status_code == 200:
            print(f"[SUCCESS] Created: {address}")
            save_wallet(mnemonic, address, private_key)
            return True
        print(f"[FAILED] {response.status_code}: {response.text}")
        return False
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

# ==============================================
# MAIN EXECUTION
# ==============================================
def main():
    while True:
        try:
            proxy = next(proxies_pool)
            print(f"Using proxy: {proxy}")
            create_account(proxy)
            time.sleep(REQUEST_DELAY + random.uniform(0, 3))
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            break

if __name__ == "__main__":
    main()
