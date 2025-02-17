# Kite AI Automation

An automated script for interacting with Kite AI Assistant and Crypto Price Assistant on the Kite AI testnet platform.

## Features
- Automated interaction with multiple Kite AI agents
- Point accumulation system (up to 200 points daily)
- Intelligent question rotation
- Proxy support
- Automatic session management
- Rate limiting and error handling
- Detailed statistics tracking

## Prerequisites

### System Requirements
- Python 3.7 or higher
- pip (Python package installer)
- Internet connection
- (Optional) Proxy service

### Required Python Packages
```bash
pip install requests colorama urllib3
```

Or install all requirements at once using:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone or download the repository:
```bash
git clone https://github.com/yourusername/kite-ai-automation.git
cd kite-ai-automation
```

2. Create a requirements.txt file with the following content:
```
requests>=2.26.0
colorama>=0.4.4
urllib3>=1.26.7
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the bot, you may want to modify these settings in the code:

1. Wallet Configuration:
```python
DEFAULT_WALLET = "YOUR_ADDRESS"
```

2. Proxy Configuration:
```python
PROXIES = {
    "YOUR_PROXY_HTTP/SOCKS5"
}
```

3. Point System Settings:
```python
MAX_DAILY_POINTS = 200
POINTS_PER_INTERACTION = 10
MAX_DAILY_INTERACTIONS = 20
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. When prompted, enter your wallet address or press Enter to use the default wallet.

3. The bot will automatically:
   - Rotate between AI assistants
   - Ask predefined questions
   - Track points and interactions
   - Handle errors and retries
   - Report usage statistics

## Troubleshooting

### Common Issues

1. Connection Timeout Error
```
Error: HTTPSConnectionPool(host='quests-usage-dev.prod.zettablock.com', port=443): Read timed out. (read timeout=15)
```
**Solution**: This is a known issue with the usage tracking server. The bot continues to function normally despite this error. No action required.

2. Proxy Connection Issues
- Verify your proxy configuration in the PROXIES variable
- Ensure your proxy service is active
- Check proxy credentials if required

3. Rate Limiting
- The bot includes automatic handling for rate limits
- Built-in cooldown periods between requests
- Exponential backoff for retries

### Error Prevention

1. Always use a stable internet connection
2. Configure proper proxy settings if required
3. Don't modify the cooldown and retry settings unless necessary
4. Keep Python and required packages updated

## Safety Features

1. Rate Limiting Protection:
- Automatic cooldown periods
- Exponential backoff for retries
- Maximum retry attempts

2. Session Management:
- Unique session IDs
- Device fingerprinting
- Automatic session recovery

3. Error Handling:
- Connection timeout handling
- Rate limit management
- Critical error recovery
- Graceful shutdown

## Monitoring

The bot provides real-time statistics:
- Current points earned
- Total interactions
- Success/failure rates
- Session duration
- Agent usage statistics

## Best Practices

1. Operation:
- Run the bot on a stable network
- Use a reliable proxy service if needed
- Monitor the bot initially to ensure proper operation

2. Maintenance:
- Regularly update Python packages
- Check for script updates
- Monitor proxy health if using proxies

3. Performance:
- Don't modify default timings unless necessary
- Keep logs for troubleshooting
- Monitor system resources

## Support

For issues and updates:
1. Check the troubleshooting section
2. Report issues through GitHub
3. Check for script updates regularly

## Disclaimer

This automation tool is not officially associated with Kite AI. Use at your own discretion and ensure compliance with all relevant terms of service.