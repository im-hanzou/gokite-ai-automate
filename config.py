import sys
import codecs
import locale
from datetime import datetime

# Set UTF-8 encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

# Wallet Configuration
DEFAULT_WALLET = "0x6646de28934127ba20ea5444206cfd1c382a7c17"  # Your wallet address

# Points Configuration
MAX_DAILY_POINTS = 200
POINTS_PER_INTERACTION = 10
MAX_DAILY_INTERACTIONS = 20

# AI Endpoints Configuration
AI_ENDPOINTS = {
    "https://deployment-nc3y3k7zy6gekszmcsordhu7.stag-vxzy.zettablock.com/main": {
        "name": "Kite AI Assistant",
        "agent_id": "deployment_nc3y3k7zy6gekszmcsordhu7",
        "questions": [
            "What is blockchain technology?",
            "How do smart contracts work?",
            "What are the advantages of DeFi?",
            "Can you explain what NFTs are?",
            "How does cryptocurrency mining work?",
            "What is the difference between proof of work and proof of stake?",
            "What are the main use cases of blockchain?",
            "How does blockchain ensure security?",
            "What is decentralization?",
            "How do cryptocurrency wallets work?",
        ],
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "name": "Blockchain Expert",
        "agent_id": "deployment_sofftlsf9z4fya3qchykaanq",
        "questions": [
            "What are the fundamental principles of blockchain?",
            "How does consensus mechanism work?",
            "What is the role of cryptography in blockchain?",
            "Can you explain what is a blockchain fork?",
            "What are the benefits of decentralization?",
            "How do public and private keys work?",
            "What is the purpose of a whitepaper?",
            "How does blockchain maintain transparency?",
            "What are layer 2 scaling solutions?",
            "What are the environmental impacts of blockchain?",
        ],
    },
}

# Banner Configuration
BANNER = """
+==========================================+
|              KITE AI AUTOMATE            |
|       Github: github.com/im-hanzou       |
+==========================================+
"""
