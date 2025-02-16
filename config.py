import sys
import codecs
import locale
from datetime import datetime
from colorama import Fore, Style

# Set UTF-8 encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

# Global configuration
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
            "What are the use cases for Kite AI?",
        ],
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
            "Price prediction for ADA",
        ],
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_SoFftlsf9z4fyA3QCHYkaANq",
        "name": "Transaction Analyzer",
        "questions": [],
    },
}

# Wallet Configuration
DEFAULT_WALLET = "0x6646xxxxxxxxxxxxxxxxxxx7c17"

# Points and Interactions Configuration
MAX_DAILY_POINTS = 1000
POINTS_PER_INTERACTION = 50
MAX_DAILY_INTERACTIONS = 20

# AI Endpoints Configuration
AI_ENDPOINTS = {
    "https://deployment-nc3y3k7zy6gekszmcsordhu7.stag-vxzy.zettablock.com/main": {
        "name": "Crypto Price Assistant",
        "agent_id": "price_assistant",
        "questions": [
            "Show me Ethereum price trends",
            "What's the current Bitcoin price?",
            "How has the crypto market performed today?",
        ],
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "name": "Transaction Analyzer",
        "agent_id": "tx_analyzer",
        "questions": [],  # Will be populated dynamically
    },
}

# Banner Configuration
BANNER = """
+==========================================+
|              KITE AI AUTOMATE            |
|       Github: github.com/im-hanzou       |
+==========================================+
"""
