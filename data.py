# data.py

# Live platform inventory and system parameters
PLATFORM_DB = {
    "auctions": [
        {"id": "A1", "item": "MacBook Pro M3 Max", "bid": 125000, "status": "Active"},
        {"id": "A2", "item": "Sony PlayStation 5", "bid": 45000, "status": "Closing Soon"},
        {"id": "A3", "item": "Sony Alpha A7 IV", "bid": 108000, "status": "Active"}
    ],
    "platform_rules": "Minimum increment ₹500. 7-Day return policy."
}

# Verified buyer profile metrics
BUYER_DB = {
    "name": "Harsh Gond",
    "tier": "Verified Buyer",
    "stats": {"won": 18, "active_bids": 2},
    "wallet_balance": 150000
}

# Verified seller metrics and listing inventory
SELLER_DB = {
    "name": "Aarav Sharma",
    "tier": "Top Rated Seller",
    "stats": {"active_listings": 24, "total_revenue": 1842500},
    "pending_drafts": ["Vintage Rolex Watch", "Canon EOS R5"]
}