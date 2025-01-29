import os
import time
import requests
import random
from itertools import cycle
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins
from fake_useragent import UserAgent

# ==============================================
# CONFIGURATION (UPDATE THESE VALUES)
# ==============================================
REFERRAL_CODE = "YOUR_REFERRAL_CODE_HERE"  # Replace with your code
PROXIES_FILE = "proxies.txt"  # Proxies file (one per line: http://user:pass@ip:port)
API_SIGNUP_URL = "https://testnet.humanity.org/api/signup"  # Verify actual API endpoint
WALLETS_DIR = "wallets"  # Folder to store wallet data
REQUEST_DELAY = 3  # Seconds between requests (avoid rate limits)

# ==============================================
# WALLET GENERATION
# ==============================================
def generate_wallet():
    """Generate BIP44-compliant wallet (mnemonic, address, private key)."""
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)  # Change coin if needed
    return (
        mnemonic,
        bip44_mst.PublicKey().ToAddress(),
        bip44_mst.PrivateKey().Raw().ToHex()
    )

def save_wallet(mnemonic, address, private_key):
    """Save wallet data to WALLETS_DIR/[address].txt."""
    os.makedirs(WALLETS_DIR, exist_ok=True)
    with open(os.path.join(WALLETS_DIR, f"{address}.txt"), "w") as f:
        f.write(f"Mnemonic: {mnemonic}\nAddress: {address}\nPrivate Key: {private_key}\n")

# ==============================================
# ACCOUNT CREATION
# ==============================================
def load_proxies():
    """Load proxies from file into rotating pool."""
    with open(PROXIES_FILE, "r") as f:
        return cycle([line.strip() for line in f])

proxies_pool = load_proxies()
user_agent = UserAgent()

def generate_email():
    """Generate random email address."""
    return f"user{random.randint(100000, 999999)}@tempmail.com"

def create_account(proxy):
    """Create account using proxy and save wallet data."""
    try:
        headers = {"User-Agent": user_agent.random}
        proxy_config = {"http": proxy, "https": proxy}

        # Generate wallet
        mnemonic, address, private_key = generate_wallet()

        # Customize payload per Humanity Protocol's API requirements
        payload = {
            "email": generate_email(),
            "password": "TempPass123!",
            "referral_code": REFERRAL_CODE,
            "wallet_address": address
        }

        response = requests.post(
            API_SIGNUP_URL,
            json=payload,
            headers=headers,
            proxies=proxy_config,
            timeout=15
        )

        if response.status_code == 200:
            print(f"[SUCCESS] Account + Wallet created: {address}")
            save_wallet(mnemonic, address, private_key)
            return True
        else:
            print(f"[FAILED] {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

# ==============================================
# MAIN EXECUTION
# ==============================================
def main():
    while True:
        proxy = next(proxies_pool)
        print(f"Using proxy: {proxy}")
        create_account(proxy)
        time.sleep(REQUEST_DELAY + random.uniform(0, 2))  # Randomize delay

if __name__ == "__main__":
    main()