# KiteAI Automation Tool

An automated tool for interacting with Gokite.ai testnet services to earn daily points through AI interactions.

## Platform Requirements

1. **Gokite.ai Account** 
   - Register here: https://testnet.gokite.ai?r=UjcyavBf
   - Complete all initial onboarding tasks
   - Ensure your account is in good standing

2. **EVM Wallet Address**
   - Register using EVM wallet on Avalanche Chain
   - Keep your private keys secure
   - Have enough AVAX for gas fees

3. **Complete Initial Tasks**
   - Complete all required Gokite.ai onboarding tasks
   - Verify your account status
   - Ensure you have access to all features

4. **VPS or RDP (Optional)**
   - Recommended for 24/7 operation
   - Minimum specs: 1 CPU, 1GB RAM
   - Stable internet connection required

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Madleyym/gokite-ai-automate
cd kite-automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your wallet:
   - Open `config.py`
   - Replace `DEFAULT_WALLET` with your wallet address

## Dependencies

```text
requests==2.31.0
colorama==0.4.6
urllib3==2.0.7
```

## Usage

1. Basic usage:
```bash
python main.py
```

2. Run in background (Linux):
```bash
nohup python main.py &
```

3. Run with logging:
```bash
python main.py --log-level INFO
```

## Features

- Automated AI interactions
- Smart retry mechanism
- Progress tracking
- Error handling
- Session management
- Daily limits compliance
- Real-time statistics

## Configuration

Default settings in `config.py`:
```python
MAX_DAILY_POINTS = 200
POINTS_PER_INTERACTION = 20
MAX_DAILY_INTERACTIONS = 20
```

## Logging

Logs are stored in the `logs` directory:
- Format: `kite_automation_YYYYMMDD_HHMMSS.log`
- Contains detailed operation logs
- Helps with troubleshooting

## Safety Features

- Rate limiting compliance
- Error recovery
- Session management
- IP rotation (if using proxy)
- Anti-detection measures

## Troubleshooting

Common issues and solutions:

1. Connection errors:
   - Check internet connection
   - Verify API endpoints
   - Check VPN if using one

2. Authentication errors:
   - Verify wallet address
   - Check account status
   - Ensure completed onboarding

3. Rate limiting:
   - Wait for cooldown
   - Check daily limits
   - Verify interaction timing

## Best Practices

1. Run during active hours
2. Monitor logs regularly
3. Keep software updated
4. Use stable internet connection
5. Backup configuration files

## Limitations

- Daily interaction limit: 20
- Points per interaction: 20
- Maximum daily points: 200
- Required cooldown between interactions

## Legal & Compliance

- Follow Gokite.ai terms of service
- Respect rate limits
- Don't use multiple accounts
- Comply with local regulations

## Support

For issues and support:
1. Check existing issues
2. Review logs
3. Create detailed bug reports
4. Join community channels

## Updates

Check for updates regularly:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create pull request


## Disclaimer

This tool is for educational purposes only. Use at your own risk. Always comply with Gokite.ai terms of service and local regulations.