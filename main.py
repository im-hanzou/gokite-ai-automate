import requests
import json
import random
import time
import logging
import string
import platform
import uuid
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Initialize colorama
init(autoreset=True)

# Configuration
MAX_DAILY_POINTS = 200
POINTS_PER_INTERACTION = 200
MAX_DAILY_INTERACTIONS = 20
DEFAULT_WALLET = (
    "0x6xxxxxxxxc17"  # Replace with your wallet address
)

AI_ENDPOINTS = {
    "https://deployment-uu9y1z4z85rapgwkss1muuiz.stag-vxzy.zettablock.com/main": {
        "name": "Kite Blockchain Analyzer",
        "agent_id": "agent_blockchain",
        "questions": [
            "What are the recent trends in blockchain transactions?",
            "How does the current transaction volume compare to historical averages?",
            "What patterns do you see in recent smart contract interactions?",
        ],
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "name": "Transaction Analyzer",
        "agent_id": "agent_transaction",
        "questions": [],  # Will be populated with recent transaction questions
    },
}


class SecureKiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.session_id = str(uuid.uuid4())
        self.error_count = 0
        self.MAX_CONSECUTIVE_ERRORS = 5
        self.CONNECT_TIMEOUT = 30
        self.READ_TIMEOUT = 120  # Ditingkatkan dari 90
        self.MAX_RETRIES = 8    # Ditingkatkan dari 7

        # Setup components
        self._setup_logging()
        self._setup_retry_strategy()
        self._setup_session()
        self.device_fingerprint = self._generate_device_fingerprint()
        self.browser_profiles = self._load_browser_profiles()

    def _setup_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(
            log_dir, f'kite_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(console_handler)

    def _setup_retry_strategy(self):
        """Enhanced retry strategy with longer timeouts"""
        self.retry_strategy = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=2.5,    # Ditingkatkan dari 2
            status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 524],
            allowed_methods=["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE"],
            respect_retry_after_header=True
        )

    def _setup_session(self):
        """Enhanced session setup with improved timeout handling"""
        self.session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=self.retry_strategy,
            pool_connections=15,    # Ditingkatkan dari 10
            pool_maxsize=25,        # Ditingkatkan dari 20
            pool_block=False
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.timeout = (self.CONNECT_TIMEOUT, self.READ_TIMEOUT)

    def _generate_device_fingerprint(self) -> str:
        components = [
            platform.system(),
            platform.machine(),
            platform.processor(),
            str(uuid.getnode()),
            platform.python_version(),
            "".join(random.choices(string.ascii_letters + string.digits, k=16)),
        ]
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, "-".join(components)))

    def _load_browser_profiles(self) -> List[Dict]:
        return [
            {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "accept_language": "en-US,en;q=0.9",
            },
            {
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
                "accept_language": "en-GB,en;q=0.9",
            },
        ]

    def generate_headers(self) -> Dict:
        profile = random.choice(self.browser_profiles)
        return {
            "User-Agent": profile["user_agent"],
            "Accept-Language": profile["accept_language"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "X-Device-Fingerprint": self.device_fingerprint,
            "X-Session-ID": self.session_id,
        }

    def check_connection(self) -> bool:
        try:
            response = self.session.get(
                "https://testnet.kitescan.ai/api/v2/transactions",
                headers=self.generate_headers(),
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"{Fore.RED}Connection check failed: {str(e)}{Style.RESET_ALL}")
            return False

    def get_recent_transactions(self) -> List[str]:
        try:
            response = requests.get(
                "https://testnet.kitescan.ai/api/v2/advanced-filters",
                params={"transaction_types": "coin_transfer", "age": "5m"},
                headers=self.generate_headers(),
            )
            data = response.json()
            return [item["hash"] for item in data.get("items", [])]
        except Exception as e:
            print(f"{Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> Optional[str]:
        """Improved AI query function with better error handling"""
        max_attempts = 3
        base_wait_time = 5

        for attempt in range(max_attempts):
            try:
                print(f"\n{Fore.CYAN}Sending query to {AI_ENDPOINTS[endpoint]['name']} (Attempt {attempt + 1}/{max_attempts})...{Style.RESET_ALL}")

                response = self.session.post(
                    endpoint,
                    headers=self.generate_headers(),
                    json={
                        "message": message,
                        "timestamp": int(time.time()),
                        "client_info": {
                            "session_id": self.session_id,
                            "device_fingerprint": self.device_fingerprint
                        }
                    },
                    timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT)
                )

                if response.status_code == 200:
                    return response.json().get("response", "")

                wait_time = base_wait_time * (attempt + 1)
                print(f"{Fore.YELLOW}Request failed with status {response.status_code}. Waiting {wait_time} seconds before retry...{Style.RESET_ALL}")
                time.sleep(wait_time)

            except (ReadTimeout, Timeout) as e:
                wait_time = base_wait_time * (attempt + 1)
                print(f"{Fore.RED}Timeout error: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Waiting {wait_time} seconds before retry...{Style.RESET_ALL}")
                time.sleep(wait_time)

            except ConnectionError as e:
                wait_time = base_wait_time * (attempt + 1)
                print(f"{Fore.RED}Connection error: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Waiting {wait_time} seconds before retry...{Style.RESET_ALL}")
                time.sleep(wait_time)

            except Exception as e:
                wait_time = base_wait_time * (attempt + 1)
                print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Waiting {wait_time} seconds before retry...{Style.RESET_ALL}")
                time.sleep(wait_time)

        print(f"{Fore.RED}Failed to send query after {max_attempts} attempts{Style.RESET_ALL}")
        return None

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        try:
            data = {
                "wallet_address": self.wallet_address,
                "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
                "request_text": message,
                "response_text": response,
                "request_metadata": {
                    "timestamp": int(time.time()),
                    "session_id": self.session_id,
                },
            }

            response = self.session.post(
                "https://quests-usage-dev.prod.zettablock.com/api/report_usage",
                headers=self.generate_headers(),
                json=data,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"{Fore.RED}Error reporting usage: {str(e)}{Style.RESET_ALL}")
            return False

    def perform_interaction(self) -> bool:
        """Enhanced interaction function with connection checks"""
        try:
            # Check connection before proceeding
            if not self.check_connection():
                print(
                    f"{Fore.YELLOW}Connection check failed. Waiting before retry...{Style.RESET_ALL}"
                )
                time.sleep(10)
                return False

            # Rest of the function remains the same...
            transactions = self.get_recent_transactions()
            if not transactions:
                print(
                    f"{Fore.YELLOW}No recent transactions found. Waiting...{Style.RESET_ALL}"
                )
                time.sleep(5)
                return False

            AI_ENDPOINTS[
                "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main"
            ]["questions"] = [
                f"What do you think of this transaction? {tx}" for tx in transactions
            ]

            endpoint = random.choice(list(AI_ENDPOINTS.keys()))
            question = random.choice(AI_ENDPOINTS[endpoint]["questions"])

            response = self.send_ai_query(endpoint, question)
            if response and self.report_usage(endpoint, question, response):
                self.daily_points += POINTS_PER_INTERACTION
                print(
                    f"{Fore.GREEN}Interaction successful (+{POINTS_PER_INTERACTION} points){Style.RESET_ALL}"
                )
                return True
            return False

        except Exception as e:
            print(f"{Fore.RED}Error in interaction: {str(e)}{Style.RESET_ALL}")
            return False

    def run(self):
        print(f"{Fore.GREEN}Starting KiteAI automation...{Style.RESET_ALL}")
        consecutive_failures = 0

        while True:
            try:
                stats = self.check_stats()
                current_interactions = stats.get("total_interactions", 0)

                if current_interactions >= MAX_DAILY_INTERACTIONS:
                    print(f"{Fore.GREEN}Daily target reached!{Style.RESET_ALL}")
                    break

                if self.perform_interaction():
                    consecutive_failures = 0
                    time.sleep(random.uniform(10, 20))
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= self.MAX_CONSECUTIVE_ERRORS:
                        print(
                            f"{Fore.RED}Too many consecutive failures. Stopping...{Style.RESET_ALL}"
                        )
                        break
                    time.sleep(min(2**consecutive_failures, 60))

            except KeyboardInterrupt:
                print(f"{Fore.YELLOW}Stopped by user{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                consecutive_failures += 1
                if consecutive_failures >= self.MAX_CONSECUTIVE_ERRORS:
                    break
                time.sleep(min(2**consecutive_failures, 60))

    def check_stats(self) -> Dict:
        try:
            response = self.session.get(
                f"https://quests-usage-dev.prod.zettablock.com/api/user/{self.wallet_address}/stats",
                headers=self.generate_headers(),
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"{Fore.RED}Error checking stats: {str(e)}{Style.RESET_ALL}")
        return {"total_points": 0, "total_interactions": 0}


def main():
    try:
        automation = SecureKiteAIAutomation(DEFAULT_WALLET)
        if automation.check_connection():
            automation.run()
        else:
            print(f"{Fore.RED}Unable to establish connection{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Critical error: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Critical error in main: {str(e)}")


if __name__ == "__main__":
    main()
