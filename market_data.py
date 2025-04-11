import requests

DEFI_LLAMA_API = "https://api.llama.fi/protocols"

def get_filtered_protocols(min_tvl=1000000):
    response = requests.get(DEFI_LLAMA_API)

    if response.status_code != 200:
        raise Exception("Failed to fetch from DeFi Llama")

    all_protocols = response.json()
    filtered = []

    for p in all_protocols:
        if (
            "ethereum" in [c.lower() for c in p.get("chains", [])] and
            p.get("tvl", 0) > min_tvl and
            p.get("category", "").lower() in ["lending", "staking"] and
            p.get("status", "").lower() != "inactive"
        ):
            filtered.append({
                "name": p["name"],
                "category": p["category"],
                "tvl": p["tvl"],
                "chain": p["chains"],
                "url": p.get("url"),
                "symbol": p.get("symbol", "N/A")
            })

    return filtered
