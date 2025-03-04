import requests
from bs4 import BeautifulSoup
import json

def fetch_airdrops(filter_network=None, min_reward=0):
    url = "https://airdrops.io/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Request error from airdrops.io")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    airdrops = []
    
    for card in soup.select(".airdrop-card"):
        title = card.select_one(".airdrop-title").text.strip()
        reward = card.select_one(".reward").text.strip() if card.select_one(".reward") else "N/A"
        network = card.select_one(".network").text.strip() if card.select_one(".network") else "Unknown"
        link = card.select_one("a")["href"]
        
        # Convert reward to number if possible
        reward_value = float(reward.replace("$", "").replace(",", "")) if reward.replace("$", "").replace(",", "").replace(".", "").isdigit() else 0
        
        # Apply filters
        if filter_network and filter_network.lower() not in network.lower():
            continue
        if reward_value < min_reward:
            continue
        
        airdrops.append({
            "title": title,
            "reward": reward,
            "network": network,
            "link": link
        })
    
    return airdrops

if __name__ == "__main__":
    network_filter = "Ethereum"  # Change to None to disable filtering
    min_reward = 10  # Change to 0 to disable reward filtering
    airdrop_data = fetch_airdrops(filter_network=network_filter, min_reward=min_reward)
    print(json.dumps(airdrop_data, indent=4, ensure_ascii=False))
