import json

data = {       "users": [],
    "active_users": [],
    "banned_users": [],
    "inactive_users": [],
    "valid_referral_list": {},
    "unverified_referrals": {},
    "referby": {},
    "balance": {},
    "wallet": {},
    "total_withdrawals": 0,
    "total_user_withdrawals": {},
    "games_played": {},
    "last_date_entry": {},
    "total_earnings": {},
    "online_users": 0,
    "offline_users": 0,
    "verified": {},
    }

with open("data.json","w") as f:
    json.dump(data,f,indent=4)