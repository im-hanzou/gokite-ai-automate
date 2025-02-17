import requests
import json
import os
import random
import time
from typing import Dict, List
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

init(autoreset=True)

def read_wallet_address_from_file(file_path: str) -> str:
    """
    Membaca alamat wallet dari file konfigurasi.
    Mendukung format .env dan tokens.txt.
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # Cek format .env
    if '=' in content:
        key, value = content.split('=', 1)
        if key.strip().upper() == "WALLET_ADDRESS":
            return value.strip()

    # Format lain (misalnya tokens.txt)
    return content.strip()

# Global Headers
GLOBAL_HEADERS = {
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://agents.testnet.gokite.ai',
    'Referer': 'https://agents.testnet.gokite.ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

AI_ENDPOINTS = {
    "https://deployment-hp4y88pxnqxwlmpxllicjzzn.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_Hp4Y88pxNQXwLMPxlLICJZzN",
        "name": "Kite AI Assistant",
        "questions": [
            "What is Kite AI?",
            "How does Kite AI help developers?",
            "What are the main features of Kite AI?",
            "Can you explain the Kite AI ecosystem?",
            "How do I get started with Kite AI?",
            "What are the benefits of using Kite AI?",
            "How does Kite AI compare to other AI platforms?",
            "What kind of problems can Kite AI solve?",
            "Tell me about Kite AI's architecture",
            "What are the use cases for Kite AI?"
        ]
    },
    "https://deployment-nc3y3k7zy6gekszmcsordhu7.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_nC3y3k7zy6gekSZMCSordHu7",
        "name": "Crypto Price Assistant",
        "questions": [
            "Price of solana",
            "What's the current price of Bitcoin?",
            "Show me Ethereum price trends",
            "Top gainers in the last 24 hours?",
            "Which coins are trending now?",
            "Price analysis for DOT",
            "How is AVAX performing?",
            "Show me the price of MATIC",
            "What's the market cap of BNB?",
            "Price prediction for ADA"
        ]
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_SoFftlsf9z4fyA3QCHYkaANq",
        "name": "Transaction Analyzer",
        "questions": []
    }
}

class KiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION

    def reset_daily_points(self):
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            print(f"{self.print_timestamp()} {Fore.GREEN}Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            return True
        return False

    def should_wait_for_next_reset(self):
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"{self.print_timestamp()} {Fore.YELLOW}Daily point limit reached ({self.MAX_DAILY_POINTS}){Style.RESET_ALL}")
                print(f"{self.print_timestamp()} {Fore.YELLOW}Waiting until next reset at {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                time.sleep(wait_seconds)
                self.reset_daily_points()
            return True
        return False

    def print_timestamp(self):
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Style.RESET_ALL}"

    def get_recent_transactions(self) -> List[str]:
        print(f"{self.print_timestamp()} {Fore.BLUE}Fetching recent transactions...{Style.RESET_ALL}")
        url = 'https://testnet.kitescan.ai/api/v2/transactions'
        params = {
            'filter': 'validated'
        }
        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            hashes = [item['hash'] for item in data.get('items', [])]
            print(f"{self.print_timestamp()} {Fore.MAGENTA}Successfully fetched {len(hashes)} transactions{Style.RESET_ALL}")
            return hashes
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> str:
        headers = GLOBAL_HEADERS.copy()
        headers['Accept'] = 'text/event-stream'
        
        data = {
            "message": message,
            "stream": True
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=data, stream=True)
            accumulated_response = ""
            
            print(f"{Fore.CYAN}AI Response: {Style.RESET_ALL}", end='', flush=True)
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            json_str = line[6:]
                            if json_str == '[DONE]':
                                break
                            
                            json_data = json.loads(json_str)
                            content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            if content:
                                accumulated_response += content
                                print(Fore.MAGENTA + content + Style.RESET_ALL, end='', flush=True)
                        except json.JSONDecodeError:
                            continue
            
            print() 
            return accumulated_response.strip()
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error in AI query: {e}{Style.RESET_ALL}")
            return ""

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        print(f"{self.print_timestamp()} {Fore.BLUE}Reporting usage...{Style.RESET_ALL}")
        url = 'https://quests-usage-dev.prod.zettablock.com/api/report_usage'
        
        headers = GLOBAL_HEADERS.copy()
        
        data = {
            "wallet_address": self.wallet_address,
            "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
            "request_text": message,
            "response_text": response,
            "request_metadata": {}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error reporting usage: {e}{Style.RESET_ALL}")
            return False

    def check_stats(self) -> Dict:
        url = f'https://quests-usage-dev.prod.zettablock.com/api/user/{self.wallet_address}/stats'
        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error checking stats: {e}{Style.RESET_ALL}")
            return {}

    def print_stats(self, stats: Dict):
        print(f"\n{Fore.CYAN}=== Current Statistics ==={Style.RESET_ALL}")
        print(f"Total Interactions: {Fore.GREEN}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"Total Agents Used: {Fore.GREEN}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
        print(f"First Seen: {Fore.YELLOW}{stats.get('first_seen', 'N/A')}{Style.RESET_ALL}")
        print(f"Last Active: {Fore.YELLOW}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")

    def run(self):
        print(f"{self.print_timestamp()} {Fore.GREEN}Starting AI interaction script with 24-hour limits (Press Ctrl+C to stop){Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}Wallet Address: {Fore.MAGENTA}{self.wallet_address}{Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}Daily Point Limit: {self.MAX_DAILY_POINTS} points ({self.MAX_DAILY_INTERACTIONS} interactions){Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}First reset will be at: {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        interaction_count = 0
        try:
            while True:
                self.reset_daily_points()
                self.should_wait_for_next_reset()
                
                interaction_count += 1
                print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Interaction #{interaction_count}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Points: {self.daily_points + self.POINTS_PER_INTERACTION}/{self.MAX_DAILY_POINTS} | Next Reset: {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                
                transactions = self.get_recent_transactions()
                AI_ENDPOINTS["https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main"]["questions"] = [
                    f"What do you think of this transaction? {tx}"
                    for tx in transactions
                ]

                endpoint = random.choice(list(AI_ENDPOINTS.keys()))
                question = random.choice(AI_ENDPOINTS[endpoint]["questions"])
                
                print(f"\n{Fore.CYAN}Selected AI Assistant: {Fore.WHITE}{AI_ENDPOINTS[endpoint]['name']}")
                print(f"{Fore.CYAN}Agent ID: {Fore.WHITE}{AI_ENDPOINTS[endpoint]['agent_id']}")
                print(f"{Fore.CYAN}Question: {Fore.WHITE}{question}{Style.RESET_ALL}\n")
                
                initial_stats = self.check_stats()
                initial_interactions = initial_stats.get('total_interactions', 0)
                
                response = self.send_ai_query(endpoint, question)
                
                if self.report_usage(endpoint, question, response):
                    print(f"{self.print_timestamp()} {Fore.GREEN}Usage reported successfully{Style.RESET_ALL}")
                
                final_stats = self.check_stats()
                final_interactions = final_stats.get('total_interactions', 0)
                
                if final_interactions > initial_interactions:
                    print(f"{self.print_timestamp()} {Fore.GREEN}Interaction successfully recorded!{Style.RESET_ALL}")
                    self.daily_points += self.POINTS_PER_INTERACTION
                    self.print_stats(final_stats)
                else:
                    print(f"{self.print_timestamp()} {Fore.RED}Warning: Interaction may not have been recorded{Style.RESET_ALL}")
                
                delay = random.uniform(1, 3)
                print(f"\n{self.print_timestamp()} {Fore.YELLOW}Waiting {delay:.1f} seconds before next query...{Style.RESET_ALL}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n{self.print_timestamp()} {Fore.YELLOW}Script stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{self.print_timestamp()} {Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def main():
    print_banner = """
╔══════════════════════════════════════════════╗
║               KITE AIH AUTOBANG              ║
║     Github: https://github.com/arcxteam      ║
║     Github: https://github.com/im-hanzou     ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + print_banner + Style.RESET_ALL)

    # Coba baca alamat wallet dari file konfigurasi
    config_files = [".env", "tokens.txt"]
    wallet_address = None

    for file in config_files:
        wallet_address = read_wallet_address_from_file(file)
        if wallet_address:
            print(f"{Fore.GREEN}Wallet address loaded from {file}: {wallet_address}{Style.RESET_ALL}")
            break

    # Jika tidak ada file konfigurasi, minta input manual
    if not wallet_address:
        wallet_address = input(
            f"{Fore.YELLOW}Register first here: {Fore.GREEN}join https://testnet.gokite.ai/?r=Y2d9Cgy2{Fore.YELLOW} and Clear Tasks!\nNow, input your registered Wallet Address: {Style.RESET_ALL}"
        )

    # Validasi alamat wallet
    if not wallet_address:
        print(f"{Fore.RED}Error: Wallet address is required!{Style.RESET_ALL}")
        return

    automation = KiteAIAutomation(wallet_address)
    automation.run()

if __name__ == "__main__":
    main()
