import requests
import json
import random
import time
import re
from typing import Dict, List
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

init(autoreset=True)

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

class KiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION
        self.current_day_transactions = []
        self.last_transaction_fetch = None
        self.transactions_fetch_day = None 
        self.agents_config = {}
        self.usage_api_endpoint = ""
        
        self.fallback_agents = {
            "https://deployment-r89ftdnxa7jwwhyr97wq9lkg.stag-vxzy.zettablock.com/main": {
                "agent_id": "deployment_R89FtdnXa7jWWHyr97WQ9LKG",
                "name": "Professor",
                "questions": self.generate_questions_for_agent("Professor")
            },
            "https://deployment-fsegykivcls3m9nrpe9zguy9.stag-vxzy.zettablock.com/main": {
                "agent_id": "deployment_fseGykIvCLs3m9Nrpe9Zguy9",
                "name": "Crypto Buddy",
                "questions": self.generate_questions_for_agent("Crypto Buddy")
            },
            "https://deployment-xkerjnnbdtazr9e15x3y7fi8.stag-vxzy.zettablock.com/main": {
                "agent_id": "deployment_xkerJnNBdTaZr9E15X3Y7FI8",
                "name": "Sherlock",
                "questions": []
            }
        }
        
    def fetch_agent_configuration(self):
        print(f"{self.print_timestamp()} {Fore.BLUE}Fetching latest agent configuration...{Style.RESET_ALL}")
        
        try:
            main_page_response = requests.get("https://agents.testnet.gokite.ai/", headers=GLOBAL_HEADERS)
            main_page_content = main_page_response.text
            
            config_pattern = re.compile(r'/_next/static/chunks/app/layout-[a-z0-9]+\.js.*?["\']')
            config_matches = config_pattern.findall(main_page_content)
            
            self.agents_config = {}
            found_agents = False
            
            for config_file in config_matches:
                config_url = "https://agents.testnet.gokite.ai" + config_file
                
                try:
                    config_response = requests.get(config_url, headers=GLOBAL_HEADERS)
                    config_content = config_response.text
                    
                    agent_pattern = re.compile(r'id:"([^"]+)",name:"([^"]+)",endpoint:"([^"]+)"')
                    agent_matches = agent_pattern.findall(config_content)
                    
                    if agent_matches:
                        for agent_id, agent_name, agent_endpoint in agent_matches:
                            endpoint_url = agent_endpoint + "/main"
                            
                            self.agents_config[endpoint_url] = {
                                "agent_id": agent_id,
                                "name": agent_name,
                                "questions": self.generate_questions_for_agent(agent_name)
                            }
                            
                            print(f"{self.print_timestamp()} {Fore.GREEN}Added agent: {agent_name} ({agent_id}){Style.RESET_ALL}")
                            found_agents = True
                        
                        if found_agents and len(self.agents_config) >= 3:
                            break
                except Exception as e:
                    print(f"{self.print_timestamp()} {Fore.YELLOW}Error processing config file {config_url}: {e}{Style.RESET_ALL}")
                    continue
            
            if len(self.agents_config) > 0:
                print(f"{self.print_timestamp()} {Fore.GREEN}Successfully configured {len(self.agents_config)} agents{Style.RESET_ALL}")
                return True
            else:
                print(f"{self.print_timestamp()} {Fore.RED}No agents were configured, using fallback{Style.RESET_ALL}")
                self.agents_config = self.fallback_agents.copy()
                return False
                
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error fetching agent configuration: {e}{Style.RESET_ALL}")
            self.agents_config = self.fallback_agents.copy()
            return False
    
    def get_random_agent(self):
        self.fetch_agent_configuration()
            
        if self.agents_config:
            endpoint = random.choice(list(self.agents_config.keys()))
            return endpoint
        else:
            print(f"{self.print_timestamp()} {Fore.RED}No agents available!{Style.RESET_ALL}")
            return None
    
    def generate_questions_for_agent(self, agent_name: str) -> List[str]:
        if agent_name == "Professor":
            return [
                "What is Kite AI's core technology?",
                "How does Kite AI improve developer productivity?",
                "What are the key features of Kite AI's platform?",
                "How does Kite AI handle data security?",
                "What makes Kite AI different from other AI platforms?",
                "How does Kite AI integrate with existing systems?",
                "What programming languages does Kite AI support?",
                "How does Kite AI's API work?",
                "What are Kite AI's scalability features?",
                "How does Kite AI help with code quality?",
                "What is Kite AI's approach to machine learning?",
                "How does Kite AI handle version control?",
                "What are Kite AI's deployment options?",
                "How does Kite AI assist with debugging?",
                "What are Kite AI's code completion capabilities?",
                "How does Kite AI handle multiple projects?",
                "What is Kite AI's pricing structure?",
                "How does Kite AI support team collaboration?",
                "What are Kite AI's documentation features?",
                "How does Kite AI implement code reviews?",
                "What is Kite AI's update frequency?",
                "How does Kite AI handle error detection?",
                "What are Kite AI's testing capabilities?",
                "How does Kite AI support microservices?",
                "What is Kite AI's cloud infrastructure?",
                "How does Kite AI handle API documentation?",
                "What are Kite AI's code analysis features?",
                "How does Kite AI support continuous integration?",
                "What is Kite AI's approach to code optimization?",
                "How does Kite AI handle multilingual support?",
                "What are Kite AI's security protocols?",
                "How does Kite AI manage user permissions?",
                "What is Kite AI's backup system?",
                "How does Kite AI handle code refactoring?",
                "What are Kite AI's monitoring capabilities?",
                "How does Kite AI support remote development?",
                "What is Kite AI's approach to technical debt?",
                "How does Kite AI handle code dependencies?",
                "What are Kite AI's performance metrics?",
                "How does Kite AI support code documentation?",
                "What is Kite AI's approach to API versioning?",
                "How does Kite AI handle load balancing?",
                "What are Kite AI's debugging tools?",
                "How does Kite AI support code generation?",
                "What is Kite AI's approach to data validation?",
                "How does Kite AI handle error logging?",
                "What are Kite AI's testing frameworks?",
                "How does Kite AI support code deployment?",
                "What is Kite AI's approach to code maintenance?",
                "How does Kite AI handle system integration?"
            ]
        elif agent_name == "Crypto Buddy":
            return [
                "What is Bitcoin's current price?",
                "Show me Ethereum price",
                "What's the price of BNB?",
                "Current Solana price?",
                "What's AVAX trading at?",
                "Show me MATIC price",
                "Current price of DOT?",
                "What's the XRP price now?",
                "Show me ATOM price",
                "What's the current LINK price?",
                "Show me ADA price",
                "What's NEAR trading at?",
                "Current price of FTM?",
                "What's the ALGO price?",
                "Show me DOGE price",
                "What's SHIB trading at?",
                "Current price of UNI?",
                "What's the AAVE price?",
                "Show me LTC price",
                "What's ETC trading at?",
                "Show me the price of SAND",
                "What's MANA's current price?",
                "Current price of APE?",
                "What's the GRT price?",
                "Show me BAT price",
                "What's ENJ trading at?",
                "Current price of CHZ?",
                "What's the CAKE price?",
                "Show me VET price",
                "What's ONE trading at?",
                "Show me the price of GALA",
                "What's THETA's current price?",
                "Current price of ICP?",
                "What's the FIL price?",
                "Show me EOS price",
                "What's XTZ trading at?",
                "Show me the price of ZIL",
                "What's WAVES current price?",
                "Current price of KSM?",
                "What's the DASH price?",
                "Show me NEO price",
                "What's XMR trading at?",
                "Show me the price of IOTA",
                "What's EGLD's current price?",
                "Current price of COMP?",
                "What's the SNX price?",
                "Show me MKR price",
                "What's CRV trading at?",
                "Show me the price of RUNE",
                "What's 1INCH current price?"
            ]
        elif agent_name == "Sherlock":
            return []
        
        return ["What can you tell me about Kite AI?"]

    def reset_daily_points(self):
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            print(f"{self.print_timestamp()} {Fore.GREEN}Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            self.current_day_transactions = []
            self.last_transaction_fetch = None
            self.transactions_fetch_day = None
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

    def get_recent_transactions(self, for_sherlock=False) -> List[str]:
        current_day = datetime.now().date()
        
        if self.transactions_fetch_day == current_day and self.current_day_transactions:
            if for_sherlock:
                print(f"{self.print_timestamp()} {Fore.BLUE}Using cached transactions for today{Style.RESET_ALL}")
            return self.current_day_transactions
            
        if for_sherlock:
            print(f"{self.print_timestamp()} {Fore.BLUE}Fetching new transactions for today{Style.RESET_ALL}")
        
        url = 'https://testnet.kitescan.ai/api/v2/transactions'
        params = {
            'filter': 'validated',
            'age': '1m'
        }        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            hashes = [item['hash'] for item in data.get('items', [])]
            self.current_day_transactions = hashes
            self.last_transaction_fetch = datetime.now()
            self.transactions_fetch_day = current_day 
            if for_sherlock:
                print(f"{self.print_timestamp()} {Fore.MAGENTA}Successfully fetched {len(hashes)} transactions{Style.RESET_ALL}")
            return hashes
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> tuple:
        headers = GLOBAL_HEADERS.copy()
        headers['Accept'] = 'text/event-stream'
        
        data = {
            "message": message,
            "stream": True
        }
        
        ttft = 0
        total_time = 0
        
        print(f"{self.print_timestamp()} {Fore.BLUE}Sending question to AI Agent: {Fore.MAGENTA}{message}{Style.RESET_ALL}")
        start_time = time.time()
        first_token_received = False
        timed_out = False
        
        try:
            response = requests.post(endpoint, headers=headers, json=data, stream=True, timeout=60)
            accumulated_response = ""
                    
            print(f"\n{Fore.CYAN}AI Agent Response: {Style.RESET_ALL}", end='', flush=True)
            
            max_end_time = start_time + 60
            
            for line in response.iter_lines():
                if time.time() > max_end_time:
                    print(f"\n{self.print_timestamp()} {Fore.RED}Response timed out after 1 minute. Moving to next interaction.{Style.RESET_ALL}")
                    timed_out = True
                    break
                    
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
                                if not first_token_received:
                                    ttft = (time.time() - start_time) * 1000
                                    first_token_received = True
                                
                                accumulated_response += content
                                print(Fore.MAGENTA + content + Style.RESET_ALL, end='', flush=True)
                        except json.JSONDecodeError:
                            continue
                        
            total_time = (time.time() - start_time) * 1000
            print("\n") 

            return accumulated_response.strip(), ttft, total_time, timed_out
        except requests.exceptions.Timeout:
            print(f"\n{self.print_timestamp()} {Fore.RED}Request timed out after 1 minutes. Moving to next interaction.{Style.RESET_ALL}")
            return "", 0, 0, True 
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error in AI query: {e}{Style.RESET_ALL}")
            return "", 0, 0, True

    def report_usage(self, endpoint: str, message: str, response: str, ttft: float, total_time: float) -> bool:
        print(f"{self.print_timestamp()} {Fore.BLUE}Reporting usage...{Style.RESET_ALL}")
        
        url = f'{self.usage_api_endpoint}/report_usage' if self.usage_api_endpoint else 'https://quests-usage-dev.prod.zettablock.com/api/report_usage'
        
        headers = GLOBAL_HEADERS.copy()
        
        data = {
            "wallet_address": self.wallet_address,
            "agent_id": self.agents_config[endpoint]["agent_id"],
            "request_text": message,
            "response_text": response,
            "ttft": ttft,
            "total_time": total_time,
            "request_metadata": {}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"{self.print_timestamp()} {Fore.RED}Error reporting usage: {e}{Style.RESET_ALL}")
            return False

    def check_stats(self) -> Dict:
        url = f'{self.usage_api_endpoint}/user/{self.wallet_address}/stats' if self.usage_api_endpoint else f'https://quests-usage-dev.prod.zettablock.com/api/user/{self.wallet_address}/stats'
        
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
        print("")
        print(f"{self.print_timestamp()} {Fore.GREEN}Starting AI interaction script with 24-hour limits (Press Ctrl+C to stop){Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}Wallet Address: {Fore.MAGENTA}{self.wallet_address}{Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}Daily Point Limit: {self.MAX_DAILY_POINTS} points ({self.MAX_DAILY_INTERACTIONS} interactions){Style.RESET_ALL}")
        print(f"{self.print_timestamp()} {Fore.CYAN}First reset will be at: {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        interaction_count = 0
        try:
            while True:
                self.reset_daily_points()
                self.should_wait_for_next_reset()
                
                endpoint = self.get_random_agent()
                if not endpoint:
                    print(f"{self.print_timestamp()} {Fore.RED}No agent available. Retrying...{Style.RESET_ALL}")
                    continue
                
                interaction_count += 1
                print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Interaction #{interaction_count}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Points: {self.daily_points + self.POINTS_PER_INTERACTION}/{self.MAX_DAILY_POINTS} | Next Reset: {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                
                sherlock_endpoints = [ep for ep, config in self.agents_config.items() if config["name"] == "Sherlock"]
                if sherlock_endpoints and endpoint in sherlock_endpoints:
                    transactions = self.get_recent_transactions(for_sherlock=True)
                    if transactions:
                        self.agents_config[endpoint]["questions"] = [
                            f"What do you think of this transaction? {tx}"
                            for tx in transactions[:5]
                        ]
                
                if not self.agents_config[endpoint]["questions"]:
                    print(f"{self.print_timestamp()} {Fore.YELLOW}No questions available for {self.agents_config[endpoint]['name']}, skipping...{Style.RESET_ALL}")
                    continue
                
                question = random.choice(self.agents_config[endpoint]["questions"])
                
                print(f"\n{Fore.CYAN}Selected AI Assistant: {Fore.WHITE}{self.agents_config[endpoint]['name']}")
                print(f"{Fore.CYAN}Agent ID: {Fore.WHITE}{self.agents_config[endpoint]['agent_id']}")
                print(f"{Fore.CYAN}Question: {Fore.WHITE}{question}{Style.RESET_ALL}\n")
                
                initial_stats = self.check_stats()
                initial_interactions = initial_stats.get('total_interactions', 0)
                
                response, ttft, total_time, timed_out = self.send_ai_query(endpoint, question)
                
                print(f"{self.print_timestamp()} {Fore.BLUE}TTFT: {ttft:.2f}ms | Total Time: {total_time:.2f}ms{Style.RESET_ALL}")
                
                if not timed_out:
                    if self.report_usage(endpoint, question, response, ttft, total_time):
                        print(f"{self.print_timestamp()} {Fore.GREEN}Usage reported successfully{Style.RESET_ALL}")
                        
                        final_stats = self.check_stats()
                        final_interactions = final_stats.get('total_interactions', 0)
                        
                        if final_interactions > initial_interactions:
                            print(f"{self.print_timestamp()} {Fore.GREEN}Interaction successfully recorded!{Style.RESET_ALL}")
                            self.daily_points += self.POINTS_PER_INTERACTION
                            self.print_stats(final_stats)
                        else:
                            print(f"{self.print_timestamp()} {Fore.RED}Warning: Interaction may not have been recorded{Style.RESET_ALL}")
                    else:
                        print(f"{self.print_timestamp()} {Fore.RED}Failed to report usage{Style.RESET_ALL}")
                else:
                    print(f"{self.print_timestamp()} {Fore.YELLOW}Skipping usage report due to timeout{Style.RESET_ALL}")
                
                delay = random.uniform(60, 120)
                print(f"\n{self.print_timestamp()} {Fore.YELLOW}Waiting {delay:.1f} seconds before next query...{Style.RESET_ALL}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n{self.print_timestamp()} {Fore.YELLOW}Script stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{self.print_timestamp()} {Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def main():
    print_banner = """
╔══════════════════════════════════════════════╗
║               KITE AI AUTOMATE               ║
║     Github: https://github.com/im-hanzou     ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + print_banner + Style.RESET_ALL)
    
    wallet_address = input(f"{Fore.YELLOW}Register first, here: {Fore.GREEN}https://testnet.gokite.ai?r=cmuST6sG{Fore.YELLOW} and Complete Tasks!\n\nNow, input your registered Wallet Address: {Style.RESET_ALL}")
    
    automation = KiteAIAutomation(wallet_address)
    automation.run()

if __name__ == "__main__":
    main()
