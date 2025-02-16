import requests
import json
import random
import time
import logging
import string
import platform
import uuid
import os
import getpass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from colorama import init, Fore, Style
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
        # Points and Interactions Configuration
        self.MAX_DAILY_POINTS = MAX_DAILY_POINTS
        self.POINTS_PER_INTERACTION = POINTS_PER_INTERACTION
        self.MAX_DAILY_INTERACTIONS = MAX_DAILY_INTERACTIONS
        
        # Initialize attributes
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.session_id = str(uuid.uuid4())
        self.interaction_count = 0

        # Initialize components
        self.setup_logging()
        self.setup_session()
        self.device_fingerprint = self.generate_device_fingerprint()
        self.browser_profiles = self.load_browser_profiles()

    def generate_device_fingerprint(self) -> str:
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
        """Setup requests session with improved retry mechanism"""
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=5,  # Increased from 3 to 5
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],  # Allow retries on both GET and POST
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=3,
            pool_maxsize=10,
            pool_block=False
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def load_browser_profiles(self) -> List[Dict]:
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
        print(f"{Fore.YELLOW}🔍 Checking services...{Style.RESET_ALL}")
        try:
            response = self.session.get(
                "https://testnet.kitescan.ai/api/v2/transactions",
                headers=self.generate_headers(),
                timeout=10,
            )
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Services are available{Style.RESET_ALL}")
                return True
            print(f"{Fore.RED}❌ Services returned status code: {response.status_code}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Error checking services: {str(e)}{Style.RESET_ALL}")
            return False

    def check_stats(self) -> Dict:
        """Check current points and interactions status with better error handling"""
        for attempt in range(3):  # Try 3 times
            try:
                url = f"https://quests-usage-dev.prod.zettablock.com/api/user/{self.wallet_address}/stats"
                response = self.session.get(
                    url, 
                    headers=self.generate_headers(), 
                    timeout=(5, 15)  # (connect timeout, read timeout)
                )

                if response.status_code == 200:
                    stats = response.json()
                    total_points = stats.get('total_points', 0)
                    total_interactions = stats.get('total_interactions', 0)
                    
                    print(f"\n{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Current Progress:{Style.RESET_ALL}")
                    print(f"Points: {Fore.GREEN}{total_points}/{self.MAX_DAILY_POINTS}{Style.RESET_ALL}")
                    print(f"Interactions: {Fore.GREEN}{total_interactions}/{self.MAX_DAILY_INTERACTIONS}{Style.RESET_ALL}")
                    if total_interactions > 0:
                        print(f"Last Active: {Fore.GREEN}{stats.get('last_active', 'Never')}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}\n")
                    return stats
                
                print(f"{Fore.YELLOW}⚠️ Attempt {attempt + 1}: Status {response.status_code}{Style.RESET_ALL}")
                if attempt < 2:  # Don't sleep on last attempt
                    time.sleep(5)
                    
            except requests.exceptions.Timeout:
                print(f"{Fore.YELLOW}⚠️ Attempt {attempt + 1}: Request timed out{Style.RESET_ALL}")
                if attempt < 2:
                    time.sleep(5)
            except requests.exceptions.ConnectionError:
                print(f"{Fore.YELLOW}⚠️ Attempt {attempt + 1}: Connection error{Style.RESET_ALL}")
                if attempt < 2:
                    time.sleep(5)
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Attempt {attempt + 1}: {str(e)}{Style.RESET_ALL}")
                if attempt < 2:
                    time.sleep(5)
        
        # If all attempts fail, return default values
        print(f"{Fore.RED}❌ Could not fetch stats after 3 attempts{Style.RESET_ALL}")
        return {
            "total_points": 0,
            "total_interactions": 0,
            "last_active": "Never"
        }


    def send_ai_query(self, endpoint: str, message: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(max_retries):
            try:
                print(f"\n{Fore.CYAN}💭 Question: {message}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Waiting for AI response... (Attempt {attempt + 1}/{max_retries}){Style.RESET_ALL}")
                
                response = self.session.post(
                    endpoint,
                    headers={
                        **self.generate_headers(),
                        "Accept": "text/event-stream",
                        "Content-Type": "application/json"
                    },
                    json={
                        "message": message,
                        "stream": True,
                        "timestamp": int(time.time()),
                        "session_id": self.session_id,
                    },
                    stream=True,
                    timeout=30
                )
                
                if response.status_code == 200:
                    accumulated_response = ""
                    print(f"{Fore.GREEN}🤖 AI Response: {Style.RESET_ALL}", end="")
                    
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                try:
                                    json_str = line[6:]
                                    if json_str == '[DONE]':
                                        break
                                        
                                    data = json.loads(json_str)
                                    content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                    if content:
                                        accumulated_response += content
                                        print(content, end="", flush=True)
                                except json.JSONDecodeError:
                                    continue
                    
                    print("\n")
                    if accumulated_response:
                        return accumulated_response.strip()
                
                if attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}Retrying... ({attempt + 2}/{max_retries}){Style.RESET_ALL}")
                    time.sleep(5)
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"{Fore.RED}Error: {str(e)}, retrying...{Style.RESET_ALL}")
                    time.sleep(5)
                else:
                    print(f"{Fore.RED}❌ All attempts failed: {str(e)}{Style.RESET_ALL}")
        
        return None

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        try:
            usage_data = {
                "wallet_address": self.wallet_address,
                "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
                "request_text": message,
                "response_text": response,
                "timestamp": int(time.time())
            }

            for attempt in range(3):
                try:
                    report_response = self.session.post(
                        "https://quests-usage-dev.prod.zettablock.com/api/report_usage",
                        headers={
                            **self.generate_headers(),
                            "Content-Type": "application/json"
                        },
                        json=usage_data,
                        timeout=15
                    )

                    if report_response.status_code == 200:
                        print(f"{Fore.GREEN}✅ Usage reported successfully{Style.RESET_ALL}")
                        return True
                        
                    if attempt < 2:
                        print(f"{Fore.YELLOW}Retrying usage report... ({attempt + 2}/3){Style.RESET_ALL}")
                        time.sleep(5)
                        
                except Exception as e:
                    if attempt < 2:
                        print(f"{Fore.YELLOW}⚠️ Retry reporting usage... ({attempt + 2}/3){Style.RESET_ALL}")
                        time.sleep(5)
                    else:
                        print(f"{Fore.RED}❌ Failed to report usage: {str(e)}{Style.RESET_ALL}")
            
            return False
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error reporting usage: {str(e)}{Style.RESET_ALL}")
            return False

    def perform_interaction(self) -> bool:
        try:
            # Get initial stats
            initial_stats = self.check_stats()
            initial_interactions = initial_stats.get('total_interactions', 0)
            
            # Select AI endpoint and question
            endpoint = random.choice(list(AI_ENDPOINTS.keys()))
            question = random.choice(AI_ENDPOINTS[endpoint]["questions"])
            
            print(f"\n{Fore.CYAN}Selected AI:{Style.RESET_ALL} {AI_ENDPOINTS[endpoint]['name']}")
            
            # Get AI response
            response = self.send_ai_query(endpoint, question)
            if not response:
                return False

            # Report usage and verify
            if self.report_usage(endpoint, question, response):
                time.sleep(2)  # Wait for stats to update
                final_stats = self.check_stats()
                final_interactions = final_stats.get('total_interactions', 0)
                
                if final_interactions > initial_interactions:
                    self.daily_points += self.POINTS_PER_INTERACTION
                    print(f"{Fore.GREEN}✅ Interaction recorded! (+{self.POINTS_PER_INTERACTION} points){Style.RESET_ALL}")
                    print(f"{Fore.GREEN}✨ Total points: {self.daily_points}{Style.RESET_ALL}")
                    return True
                    
            return False

        except Exception as e:
            print(f"{Fore.RED}❌ Error in interaction: {str(e)}{Style.RESET_ALL}")
            return False

    def print_final_stats(self):
        stats = self.check_stats()
        print(f"\n{Fore.YELLOW}═══════════ Final Summary ═══════════{Style.RESET_ALL}")
        print(f"Total Points: {Fore.GREEN}{stats.get('total_points', 0)}{Style.RESET_ALL}")
        print(f"Total Interactions: {Fore.GREEN}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"Session Duration: {Fore.GREEN}{datetime.now() - self.start_time}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}═══════════════════════════════════{Style.RESET_ALL}\n")

    def run(self):
        """Main automation loop with improved error handling"""
        print(f"\n{Fore.GREEN}🚀 Starting KiteAI automation...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target: {self.MAX_DAILY_INTERACTIONS} interactions ({self.MAX_DAILY_POINTS} points){Style.RESET_ALL}")
        
        if not self.check_service_health():
            print(f"{Fore.RED}❌ Services unavailable. Stopping...{Style.RESET_ALL}")
            return

        consecutive_failures = 0
        last_summary_time = datetime.now()

        while True:
            try:
                current_time = datetime.now()
                
                # Print progress summary every hour
                if (current_time - last_summary_time).seconds >= 3600:
                    self.check_stats()
                    last_summary_time = current_time

                # Get stats with retry mechanism
                for _ in range(3):
                    stats = self.check_stats()
                    if stats.get('total_interactions', 0) is not None:
                        break
                    time.sleep(5)
                
                current_interactions = stats.get('total_interactions', 0)
                
                if current_interactions >= self.MAX_DAILY_INTERACTIONS:
                    print(f"\n{Fore.GREEN}✨ Daily target reached! ({self.MAX_DAILY_INTERACTIONS} interactions){Style.RESET_ALL}")
                    self.print_final_stats()
                    break
                
                if self.perform_interaction():
                    consecutive_failures = 0
                    delay = random.uniform(10, 20)
                    print(f"{Fore.YELLOW}Waiting {delay:.1f} seconds...{Style.RESET_ALL}")
                    time.sleep(delay)
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        print(f"{Fore.RED}Too many failures. Checking services...{Style.RESET_ALL}")
                        if not self.check_service_health():
                            print(f"{Fore.RED}❌ Services unavailable. Stopping...{Style.RESET_ALL}")
                            break
                        consecutive_failures = 0
                    delay = min(2 ** consecutive_failures, 60)
                    print(f"{Fore.RED}Failed interaction, waiting {delay} seconds...{Style.RESET_ALL}")
                    time.sleep(delay)

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Stopped by user{Style.RESET_ALL}")
                self.print_final_stats()
                break
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                consecutive_failures += 1
                delay = min(2 ** consecutive_failures, 60)
                print(f"{Fore.RED}❌ Error occurred. Waiting {delay} seconds...{Style.RESET_ALL}")
                time.sleep(delay)

def print_session_info():
    """Print current session information"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_user = getpass.getuser()
    
    print(f"\n{Fore.YELLOW}Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {Style.RESET_ALL}{current_time}")
    print(f"{Fore.YELLOW}Current User's Login: {Style.RESET_ALL}{current_user}\n")

def main():
    try:
        print(Fore.CYAN + BANNER + Style.RESET_ALL)
        print_session_info()
        automation = SecureKiteAIAutomation(DEFAULT_WALLET)
        automation.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Program stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ An error occurred: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()