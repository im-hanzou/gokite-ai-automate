from __future__ import annotations
import sys
import json
import logging
import os
import platform
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional

import requests
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, ReadTimeout, Timeout
from urllib3.util import Retry
from datetime import datetime, timezone

# Initialize colorama
init(autoreset=True)

# Konfigurasi utama
MAX_DAILY_POINTS = 200
POINTS_PER_INTERACTION = 10
MAX_DAILY_INTERACTIONS = 20
DEFAULT_WALLET = "0x6646de28934127ba20ea5444206cfd1c382a7c17"

# Proxy configuration
PROXIES = {
    "http://arrowospff4oxrepy1q-session-vnkp2css-duration-600:n5bydwiqk4jjwffx@isp.proxies.fo:10808"
}

# Global Headers
GLOBAL_HEADERS = {
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://agents.testnet.gokite.ai",
    "Referer": "https://agents.testnet.gokite.ai/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

BASE_URLS = {
    "USAGE_API": "https://quests-usage-dev.prod.zettablock.com",
    "STATS_API": "https://quests-usage-dev.prod.zettablock.com/api/user",
}

TIMEOUT_SETTINGS = {"CONNECT": 10, "READ": 15, "RETRY_DELAY": 3}

# Update session settings
SESSION_SETTINGS = {
    "MAX_RETRIES": 3,
    "BACKOFF_FACTOR": 1,
    "STATUS_FORCELIST": [408, 429, 500, 502, 503, 504],
}

RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)

AI_ENDPOINTS = {
    "https://deployment-hp4y88pxnqxwlmpxllicjzzn.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_Hp4Y88pxNQXwLMPxlLICJZzN",
        "name": "Kite AI Assistant",
        "questions": [
            "What is Kite AI and how does it work?",
            "Can you explain the main features of Kite AI?",
            "How can developers benefit from using Kite AI?",
            "What makes Kite AI different from other platforms?",
            "Tell me about Kite AI's blockchain integration",
            "How does Kite AI help with smart contract analysis?",
            "What are the key advantages of Kite AI?",
            "Explain Kite AI's approach to blockchain data",
            "How does Kite AI ensure security?",
            "What are the latest updates in Kite AI?",
        ],
    },
    "https://deployment-nc3y3k7zy6gekszmcsordhu7.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_nC3y3k7zy6gekSZMCSordHu7",
        "name": "Crypto Price Assistant",
        "questions": [
            "What's the current price of Bitcoin?",
            "Show me Ethereum's current market status",
            "How is the crypto market performing today?",
            "Tell me about BNB's current price",
            "What's happening with Solana right now?",
            "Current market analysis for MATIC",
            "Give me an update on DOT's price",
            "What's the latest on AVAX?",
            "Current crypto market overview",
            "Latest price trends in major cryptocurrencies",
        ],
    },
}

class KiteAIAutomation:
    def __init__(self, wallet_address: str = DEFAULT_WALLET) -> None:
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.session_id = str(uuid.uuid4())
        self.device_fingerprint = self._generate_device_fingerprint()
        self.MAX_DAILY_POINTS = 200  # Total maksimal 200 poin
        self.POINTS_PER_INTERACTION = 10  # 10 poin per interaksi
        self.MAX_DAILY_INTERACTIONS = 20  # 20 interaksi total
        self.used_questions: set[str] = set()
        self.session = self._setup_session()

    def _setup_session(self) -> requests.Session:
        session = requests.Session()
        session.proxies = PROXIES
        adapter = HTTPAdapter(max_retries=RETRY_STRATEGY)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _generate_device_fingerprint(self) -> str:
        components = [platform.system(), platform.machine(), str(uuid.getnode())]
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, "-".join(components)))

    def reset_daily_points(self) -> bool:
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            print(f"{self.print_timestamp()} {Fore.GREEN}Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            return True
        return False

    def should_wait_for_next_reset(self) -> bool:
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"{self.print_timestamp()} {Fore.YELLOW}Daily point limit reached ({self.MAX_DAILY_POINTS}){Style.RESET_ALL}")
                print(f"{self.print_timestamp()} {Fore.YELLOW}Waiting until next reset at {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                time.sleep(wait_seconds)
                self.reset_daily_points()
            return True
        return False

    def print_timestamp(self) -> str:
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Style.RESET_ALL}"

    def get_unused_question(self, endpoint: str) -> str:
        available_questions = [q for q in AI_ENDPOINTS[endpoint]["questions"] if q not in self.used_questions]
        if not available_questions:
            self.used_questions.clear()
            available_questions = AI_ENDPOINTS[endpoint]["questions"]

        question = random.choice(available_questions)
        self.used_questions.add(question)
        return question

    def send_ai_query(self, endpoint: str, message: str) -> str:
        headers = GLOBAL_HEADERS.copy()
        headers.update({
            "Accept": "text/event-stream",
            "X-Device-Fingerprint": self.device_fingerprint,
            "X-Session-ID": self.session_id,
        })

        data = {
            "message": message,
            "stream": True,
            "timestamp": int(time.time()),
            "client_info": {
                "session_id": self.session_id,
                "device_fingerprint": self.device_fingerprint,
            },
        }

        try:
            response = self.session.post(
                endpoint,
                headers=headers,
                json=data,
                stream=True,
                timeout=(TIMEOUT_SETTINGS['CONNECT'], TIMEOUT_SETTINGS['READ'])
            )

            accumulated_response = ""
            print(f"{Fore.CYAN}AI Response: {Style.RESET_ALL}", end="", flush=True)

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        try:
                            json_str = line_str[6:]
                            if json_str == "[DONE]":
                                break

                            json_data = json.loads(json_str)
                            content = json_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                accumulated_response += content
                                print(Fore.MAGENTA + content + Style.RESET_ALL, end="", flush=True)
                        except json.JSONDecodeError:
                            continue

            print()
            return accumulated_response.strip()

        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error in AI query: {str(e)}{Style.RESET_ALL}")
            return ""

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        print(f"{self.print_timestamp()} {Fore.BLUE}Reporting usage...{Style.RESET_ALL}")

        headers = GLOBAL_HEADERS.copy()
        headers.update({
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Device-Fingerprint': self.device_fingerprint,
            'X-Session-ID': self.session_id,
        })

        data = {
            "wallet_address": self.wallet_address,
            "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
            "request_text": message,
            "response_text": response,
            "request_metadata": {
                "timestamp": int(time.time()),
                "session_id": self.session_id,
                "device_fingerprint": self.device_fingerprint
            }
        }

        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries):
            try:
                resp = self.session.post(
                    f"{BASE_URLS['USAGE_API']}/api/report_usage",
                    headers=headers,
                    json=data,
                    timeout=(TIMEOUT_SETTINGS['CONNECT'], TIMEOUT_SETTINGS['READ'])
                )

                if resp.status_code == 200:
                    print(f"{self.print_timestamp()} {Fore.GREEN}Usage report successful{Style.RESET_ALL}")
                    return True

                if resp.status_code == 429:  # Rate limit
                    wait_time = int(resp.headers.get('Retry-After', base_delay * (attempt + 1)))
                    print(f"{self.print_timestamp()} {Fore.YELLOW}Rate limited. Waiting {wait_time} seconds...{Style.RESET_ALL}")
                    time.sleep(wait_time)
                    continue

                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"{self.print_timestamp()} {Fore.YELLOW}Attempt {attempt + 1} failed. Waiting {delay} seconds...{Style.RESET_ALL}")
                    time.sleep(delay)
                else:
                    print(f"{self.print_timestamp()} {Fore.RED}All attempts failed{Style.RESET_ALL}")

            except Exception as e:
                print(f"{self.print_timestamp()} {Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)

        return False

    def check_stats(self) -> Dict:
        try:
            response = self.session.get(
                f"{BASE_URLS['STATS_API']}/{self.wallet_address}/stats",
                headers=GLOBAL_HEADERS,
                timeout=TIMEOUT_SETTINGS['READ']
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error checking stats: {str(e)}{Style.RESET_ALL}")
            return {}

    def print_stats(self, stats: Dict) -> None:
        print(f"\n{Fore.CYAN}=== Current Statistics ==={Style.RESET_ALL}")
        print(f"Total Interactions: {Fore.GREEN}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"Total Points: {Fore.GREEN}{self.daily_points}{Style.RESET_ALL}")
        print(f"Total Agents Used: {Fore.GREEN}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
        print(f"Last Active: {Fore.YELLOW}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")

    def run(self) -> None:
        try:
            current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n{Fore.CYAN}=== Session Information ==={Style.RESET_ALL}")
            print(f"Current Time (UTC): {Fore.GREEN}{current_time}{Style.RESET_ALL}")
            print(f"Wallet: {Fore.GREEN}{self.wallet_address}{Style.RESET_ALL}\n")

            interaction_count = 0
            consecutive_failures = 0
            MAX_CONSECUTIVE_FAILURES = 5
            retry_delay = TIMEOUT_SETTINGS['RETRY_DELAY']

            while interaction_count < MAX_DAILY_INTERACTIONS:
                try:
                    if consecutive_failures > 0:
                        cooldown = min(retry_delay * (2 ** consecutive_failures), 30)
                        print(f"{self.print_timestamp()} {Fore.YELLOW}Cooling down for {cooldown} seconds...{Style.RESET_ALL}")
                        time.sleep(cooldown)

                    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                    print(f"{Fore.MAGENTA}Interaction #{interaction_count + 1}/20{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Points: {self.daily_points}/200 ({(interaction_count + 1) * 10} expected){Style.RESET_ALL}")

                    endpoint = random.choice(list(AI_ENDPOINTS.keys()))
                    question = self.get_unused_question(endpoint)

                    print(f"\n{Fore.CYAN}Selected AI Assistant: {AI_ENDPOINTS[endpoint]['name']}")
                    print(f"{Fore.CYAN}Question: {Fore.WHITE}{question}{Style.RESET_ALL}\n")

                    response = self.send_ai_query(endpoint, question)

                    if response and len(response.strip()) > 0:
                        try:
                            self.report_usage(endpoint, question, response)
                        except:
                            pass  # Continue even if reporting fails

                        self.daily_points += self.POINTS_PER_INTERACTION
                        interaction_count += 1
                        consecutive_failures = 0

                        delay = random.uniform(8, 12)
                        print(f"\n{self.print_timestamp()} {Fore.YELLOW}Next query in {delay:.1f} seconds...{Style.RESET_ALL}")
                        time.sleep(delay)
                        continue

                    consecutive_failures += 1
                    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        print(f"{Fore.RED}Too many consecutive failures. Restarting...{Style.RESET_ALL}")
                        consecutive_failures = 0
                        time.sleep(30)

                except Exception as e:
                    print(f"{self.print_timestamp()} {Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                    consecutive_failures += 1
                    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        print(f"{Fore.RED}Critical error. Restarting...{Style.RESET_ALL}")
                        consecutive_failures = 0
                        time.sleep(30)

        except KeyboardInterrupt:
            print(f"\n{self.print_timestamp()} {Fore.YELLOW}Script stopped by user{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}=== Final Statistics ==={Style.RESET_ALL}")
            print(f"Total Interactions: {Fore.GREEN}{interaction_count}{Style.RESET_ALL}")
            print(f"Total Points: {Fore.GREEN}{self.daily_points}{Style.RESET_ALL}")
            try:
                with self.session.get(
                    f"{BASE_URLS['STATS_API']}/{self.wallet_address}/stats",
                    headers=GLOBAL_HEADERS,
                    timeout=5  # Short timeout for final stats
                ) as response:
                    if response.status_code == 200:
                        stats = response.json()
                        print(f"Total Agents Used: {Fore.GREEN}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
                        print(f"Last Active: {Fore.YELLOW}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")
            except:
                pass  # Ignore errors when getting final stats
            finally:
                print(f"\n{Fore.YELLOW}Session ended.{Style.RESET_ALL}")
                sys.exit(0)


def main() -> None:
    try:
        print_banner = """
         ₍  ˃ᯅ˂ ₎
        （ ͜•人 ͜•）
         )  •  (
         (‿ώ‿)
           ꪊꪻ
        """
        print(Fore.CYAN + print_banner + Style.RESET_ALL)

        # Get current UTC time
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"Current Date and Time (UTC): {Fore.GREEN}{current_time}{Style.RESET_ALL}"
        )

        try:
            wallet_address = (
                input(
                    f"\n{Fore.YELLOW}ENTER your registered Wallet Address "
                    f"[{Fore.GREEN}{DEFAULT_WALLET}{Fore.YELLOW}]: {Style.RESET_ALL}"
                ).strip()
                or DEFAULT_WALLET
            )

            automation = KiteAIAutomation(wallet_address)
            automation.run()

        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}Script initialization cancelled by user.{Style.RESET_ALL}"
            )
            sys.exit(0)

    except Exception as e:
        print(f"\n{Fore.RED}Fatal Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Script terminated by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
