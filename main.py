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
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from config import (
    AI_ENDPOINTS,
    DEFAULT_WALLET,
    MAX_DAILY_POINTS,
    POINTS_PER_INTERACTION,
    MAX_DAILY_INTERACTIONS,
    BANNER,
)

init(autoreset=True)


class SecureKiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = MAX_DAILY_POINTS
        self.POINTS_PER_INTERACTION = POINTS_PER_INTERACTION
        self.MAX_DAILY_INTERACTIONS = MAX_DAILY_INTERACTIONS
        self.session_id = str(uuid.uuid4())

        # Initialize components
        self.setup_logging()
        self.setup_session()
        self.device_fingerprint = self.generate_device_fingerprint()
        self.browser_profiles = self.load_browser_profiles()

    def generate_device_fingerprint(self) -> str:
        """Generate unique device fingerprint"""
        components = [
            platform.system(),
            platform.machine(),
            platform.processor(),
            str(uuid.getnode()),
            platform.python_version(),
            "".join(random.choices(string.ascii_letters + string.digits, k=16)),
        ]
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, "-".join(components)))

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(
            log_dir, f'kite_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def setup_session(self):
        """Setup requests session with retry mechanism"""
        self.session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def load_browser_profiles(self) -> List[Dict]:
        """Load browser profiles for request headers"""
        return [
            {
                "name": "Chrome Windows",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "accept_language": "en-US,en;q=0.9",
                "platform": "Windows",
            },
            {
                "name": "Firefox Mac",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
                "accept_language": "en-GB,en;q=0.9",
                "platform": "MacOS",
            },
        ]

    def generate_headers(self) -> Dict:
        """Generate request headers"""
        profile = random.choice(self.browser_profiles)
        return {
            "User-Agent": profile["user_agent"],
            "Accept-Language": profile["accept_language"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "X-Device-Fingerprint": self.device_fingerprint,
            "X-Session-ID": self.session_id,
        }

    def check_service_health(self) -> bool:
        """Check if required services are available"""
        print(f"{Fore.YELLOW}🔍 Checking services...{Style.RESET_ALL}")

        try:
            response = self.session.get(
                "https://testnet.kitescan.ai/api/health",
                headers=self.generate_headers(),
                timeout=10,
            )
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Services are available{Style.RESET_ALL}")
                return True
            else:
                print(
                    f"{Fore.RED}❌ Services returned status code: {response.status_code}{Style.RESET_ALL}"
                )
                return False
        except Exception as e:
            print(f"{Fore.RED}❌ Error checking services: {str(e)}{Style.RESET_ALL}")
            return False

    def get_transactions(self) -> List[str]:
        """Get transactions from KiteScan API"""
        try:
            response = self.session.get(
                "https://testnet.kitescan.ai/api/v2/transactions",
                headers=self.generate_headers(),
                params={"filter": "validated"},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                return [tx["hash"] for tx in data.get("items", [])][:10]
            return []
        except Exception as e:
            logging.error(f"Error getting transactions: {str(e)}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> Optional[str]:
        """Send query to AI endpoint"""
        print(f"\n{Fore.YELLOW}💭 Question: {message}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Waiting for AI response...{Style.RESET_ALL}")

        try:
            response = self.session.post(
                endpoint,
                headers={**self.generate_headers(), "Accept": "text/event-stream"},
                json={
                    "message": message,
                    "stream": True,
                    "timestamp": int(time.time()),
                    "session_id": self.session_id,
                },
                timeout=30,
            )

            if response.status_code != 200:
                return None

            content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            text = data.get("choices", [{}])[0].get("text", "")
                            if text:
                                content += text
                                print(text, end="", flush=True)
                        except json.JSONDecodeError:
                            continue

            return content
        except Exception as e:
            logging.error(f"Error in AI query: {str(e)}")
            return None

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        """Report interaction usage"""
        try:
            response = self.session.post(
                "https://quests-usage-dev.prod.zettablock.com/api/report_usage",
                headers=self.generate_headers(),
                json={
                    "wallet_address": self.wallet_address,
                    "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
                    "request_text": message,
                    "response_text": response,
                    "request_metadata": {
                        "timestamp": int(time.time()),
                        "session_id": self.session_id,
                        "device_fingerprint": self.device_fingerprint,
                    },
                },
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Error reporting usage: {str(e)}")
            return False

    def perform_interaction(self) -> bool:
        """Perform one complete interaction cycle"""
        try:
            # Get transactions
            transactions = self.get_transactions()
            if not transactions:
                print(f"{Fore.RED}❌ No transactions available{Style.RESET_ALL}")
                return False

            # Select AI endpoint and question
            endpoint = random.choice(list(AI_ENDPOINTS.keys()))
            if "Transaction Analyzer" in AI_ENDPOINTS[endpoint]["name"]:
                questions = [
                    f"What do you think of this transaction? {tx}"
                    for tx in transactions
                ]
            else:
                questions = AI_ENDPOINTS[endpoint]["questions"]

            question = random.choice(questions)

            # Send query to AI
            print(
                f"\n{Fore.CYAN}Selected AI: {AI_ENDPOINTS[endpoint]['name']}{Style.RESET_ALL}"
            )
            response = self.send_ai_query(endpoint, question)
            if not response:
                return False

            # Report usage
            if self.report_usage(endpoint, question, response):
                self.daily_points += self.POINTS_PER_INTERACTION
                print(f"\n{Fore.GREEN}✅ Interaction successful{Style.RESET_ALL}")
                return True
            return False

        except Exception as e:
            logging.error(f"Error in interaction: {str(e)}")
            return False

    def run(self):
        """Main automation loop"""
        print(f"\n{Fore.GREEN}🚀 Starting KiteAI automation...{Style.RESET_ALL}")

        if not self.check_service_health():
            return

        consecutive_failures = 0

        while True:
            try:
                current_time = datetime.now()

                # Check daily limits
                if self.daily_points >= self.MAX_DAILY_POINTS:
                    wait_time = (self.next_reset_time - current_time).total_seconds()
                    print(
                        f"\n{Fore.YELLOW}Daily points limit reached. Waiting {wait_time/3600:.1f} hours...{Style.RESET_ALL}"
                    )
                    time.sleep(min(wait_time, 3600))
                    continue

                interactions_done = self.daily_points // self.POINTS_PER_INTERACTION
                print(
                    f"\n{Fore.CYAN}Progress: {interactions_done + 1}/{self.MAX_DAILY_INTERACTIONS}{Style.RESET_ALL}"
                )

                # Perform interaction
                if self.perform_interaction():
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        print(
                            f"{Fore.RED}Too many failures. Checking services...{Style.RESET_ALL}"
                        )
                        if not self.check_service_health():
                            break
                        consecutive_failures = 0

                # Wait between interactions
                delay = random.uniform(5, 15)
                print(f"{Fore.CYAN}Waiting {delay:.1f} seconds...{Style.RESET_ALL}")
                time.sleep(delay)

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Stopped by user{Style.RESET_ALL}")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                consecutive_failures += 1
                time.sleep(min(2**consecutive_failures, 60))


def main():
    print(Fore.CYAN + BANNER + Style.RESET_ALL)
    automation = SecureKiteAIAutomation(DEFAULT_WALLET)
    automation.run()


if __name__ == "__main__":
    main()
