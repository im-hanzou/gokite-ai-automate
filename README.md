# Kite AI Automation
An automated script for interacting with Kite AI Assistant and Crypto Price Assistant on the Kite AI testnet platform.

## Features
* Automated interaction with multiple Kite AI agents
* Point accumulation system (up to 200 points daily)
* Intelligent question rotation
* Proxy support
* Automatic session management
* Rate limiting and error handling
* Detailed statistics tracking

## Known Issues
The bot may display the following error message during operation:
```
Error: HTTPSConnectionPool(host='quests-usage-dev.prod.zettablock.com', port=443): Read timed out. (read timeout=15)
```
**Note**: This is a known issue with the connection to the usage tracking server. The bot continues to function normally and accumulate points despite this error message. No action is required from users when this message appears.

## Requirements
* Python 3.7+
* Required Python packages:
   * requests
   * colorama
   * urllib3

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Madleyym/gokite-ai-automate
cd kite-ai-automation
```
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration
The script includes several configurable parameters in the code:
* `MAX_DAILY_POINTS`: Maximum points that can be earned daily (default: 200)
* `POINTS_PER_INTERACTION`: Points earned per interaction (default: 10)
* `MAX_DAILY_INTERACTIONS`: Maximum number of daily interactions (default: 20)
* `DEFAULT_WALLET`: Default wallet address
* `PROXIES`: Proxy configuration settings

## Usage
1. Run the script:
```bash
python main.py
```
2. When prompted, enter your wallet address or press Enter to use the default wallet.
3. The script will automatically:
   * Rotate between different AI assistants
   * Ask random predefined questions
   * Track points and interactions
   * Report usage statistics
   * Handle errors and retries

## Features Details

### Point System
* Each interaction earns 10 points
* Daily maximum of 200 points
* Points reset every 24 hours

### AI Assistants
1. Kite AI Assistant
   * Provides information about Kite AI platform
   * Answers technical questions
2. Crypto Price Assistant
   * Provides cryptocurrency price information
   * Market analysis and trends

### Safety Features
* Rate limiting protection
* Error handling with exponential backoff
* Session management
* Device fingerprinting
* Automatic cooldown periods

## Error Handling
The script includes comprehensive error handling:
* Connection timeout handling
* Rate limit management
* Automatic retries with exponential backoff
* Session recovery
* Critical error handling
* Graceful handling of usage tracking server timeouts

## Statistics
The script provides real-time statistics:
* Total interactions
* Points earned
* Agents used
* Last active timestamp
* Current session information

## Notes
* The script uses UTC time for all operations
* Proxy configuration is required for proper operation
* Maximum 20 interactions per 24-hour period
* Automatic cooldown between requests
* Usage tracking server timeouts do not affect bot functionality

## Troubleshooting
* If you see the timeout error message from the usage tracking server, no action is required - the bot will continue to function normally
* The error is related to the statistics tracking system and does not impact point accumulation or interaction success
* The bot includes automatic retry mechanisms for other types of errors

## Disclaimer
This script is for educational purposes only. Please ensure you comply with Kite AI's terms of service when using this automation tool.