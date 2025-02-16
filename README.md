# SecureKiteAI Automation

A secure, advanced automation script for daily Gokite.ai testnet agent interactions with enhanced anti-detection measures and human behavior simulation.

## Features

- 🔒 Advanced security measures and anti-detection system
- 🤖 Realistic human behavior simulation
- 📊 Detailed usage tracking and statistics
- 🔄 Automatic rate limiting and error handling
- 📝 Comprehensive logging system
- 🎨 Colored console output for better readability
- ⚡ Efficient request management with retry mechanisms
- 🔐 Secure session handling with device fingerprinting

## Requirements

### Platform Requirements

1. Gokite.ai Account - Register here: [https://testnet.gokite.ai](https://testnet.gokite.ai?r=TzmGkHcM)
2. EVM Wallet Address - Register using EVM wallet on Avalanche Chain
3. Complete all initial Gokite.ai tasks
4. VPS or RDP (Optional)

### Technical Requirements

- Python 3.x
- Required Python packages (installed via requirements.txt)

## Installation

### Step 1: Install Python

#### Windows
Download and install from [Python Official Website](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)

#### Unix Systems
```bash
apt install python3 python3-pip git -y
```

#### Termux
```bash
pkg install python python-pip git -y
```

### Step 2: Get the Script

Either download [manually](https://github.com/im-hanzou/gokite-ai-automate/archive/refs/heads/main.zip) or clone using git:
```bash
git clone https://github.com/im-hanzou/gokite-ai-automate
```

### Step 3: Install Dependencies

Navigate to the project directory:
```bash
cd gokite-ai-automate
```

Install required packages:
- Windows/Termux:
```bash
pip install -r requirements.txt
```
- Unix:
```bash
pip3 install -r requirements.txt
```

## Usage

### Running the Bot

#### Windows/Termux:
```bash
python main.py
```

#### Unix:
```bash
python3 main.py
```

### Configuration

When prompted, enter your EVM wallet address in the format:
```
0x123456789XXXXX123456789XXXXX1234567890
```

## Features in Detail

### Security Measures
- Advanced retry strategy with exponential backoff
- Rotating user agents and browser profiles
- Device fingerprinting
- Session tracking
- Request pattern analysis

### Automation Features
- Automatic daily points tracking
- Interaction limits management
- Transaction validation
- Real-time statistics monitoring
- Colored console output for status updates

### Error Handling
- Comprehensive error logging
- Automatic retry mechanisms
- Rate limit management
- Session timeout handling

## Monitoring

The script provides real-time statistics including:
- 💼 Wallet address
- 🔄 Total interactions
- ⭐ Points earned
- 🤖 Agents used
- 📅 First seen date
- ⏰ Last active timestamp

## Important Notes

- Using this bot is at your own risk
- This tool is for educational purposes only
- The developer is not responsible for any loss or damage
- Consider using the referral code provided if you're new to Gokite.ai

## Logs

Logs are automatically stored in the `logs` directory with timestamps for debugging and monitoring purposes.

## License

This project is provided "as is" without warranty of any kind.